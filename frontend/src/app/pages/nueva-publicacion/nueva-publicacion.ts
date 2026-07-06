import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ArticlesService } from '../../services/articles.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-nueva-publicacion',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './nueva-publicacion.html',
  styleUrl: './nueva-publicacion.scss'
})
export class NuevaPublicacionComponent implements OnInit {
  private articlesService = inject(ArticlesService);
  private router = inject(Router);
  private authService = inject(AuthService);

  public title = '';
  public content = '';
  public fpublicacion = '';

  /** URL final que se enviará al backend (puede venir de subida o de campo manual) */
  public imageUrl = '';
  /** Previsualización local del archivo seleccionado (blob URL) o la URL manual */
  public previewUrl = signal<string | null>(null);
  /** Archivo seleccionado pendiente de subir */
  private archivoSeleccionado: File | null = null;

  public isLoading = signal(false);
  public isUploadingImage = signal(false);
  public isSuccess = signal(false);
  public errorMessage = signal<string | null>(null);

  constructor() {
    const today = new Date();
    this.fpublicacion = `${today.getDate().toString().padStart(2, '0')}/${(today.getMonth() + 1).toString().padStart(2, '0')}/${today.getFullYear()}`;
  }

  ngOnInit(): void {
    if (!this.authService.isRedactor()) {
      this.router.navigate(['/dashboard']);
    }
  }

  /** Maneja la selección de archivo desde el input file */
  onArchivoSeleccionado(evento: Event): void {
    const input = evento.target as HTMLInputElement;
    const archivo = input.files?.[0];
    if (!archivo) return;

    // Previsualización local instantánea sin esperar a la subida
    const blobUrl = URL.createObjectURL(archivo);
    this.previewUrl.set(blobUrl);

    // Limpiar URL manual si el usuario selecciona un archivo
    this.imageUrl = '';
    this.archivoSeleccionado = archivo;
  }

  /** Limpia la imagen seleccionada (archivo o URL) */
  limpiarImagen(): void {
    this.archivoSeleccionado = null;
    this.imageUrl = '';
    this.previewUrl.set(null);
  }

  /** Al escribir una URL manual, descarta el archivo local */
  onUrlManualCambia(): void {
    if (this.imageUrl) {
      this.archivoSeleccionado = null;
      this.previewUrl.set(this.imageUrl);
    } else {
      this.previewUrl.set(null);
    }
  }

  onSubmit(): void {
    if (!this.title || !this.content || !this.fpublicacion) {
      this.errorMessage.set('Por favor, completa todos los campos requeridos.');
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set(null);

    // Si hay un archivo pendiente de subir, lo subimos primero
    if (this.archivoSeleccionado) {
      this.isUploadingImage.set(true);
      this.articlesService.uploadImage(this.archivoSeleccionado).subscribe({
        next: (res) => {
          this.imageUrl = res.url;
          this.isUploadingImage.set(false);
          this.guardarArticulo();
        },
        error: (err) => {
          this.isUploadingImage.set(false);
          this.isLoading.set(false);
          this.errorMessage.set('Error al subir la imagen: ' + (err.error?.detail || err.message));
        }
      });
    } else {
      this.guardarArticulo();
    }
  }

  private guardarArticulo(): void {
    const articleData = {
      title: this.title,
      content: this.content,
      status: 'BORRADOR',
      fpublicacion: this.fpublicacion,
      customPhotoUrl: this.imageUrl || null
    };

    this.articlesService.createArticle(articleData).subscribe({
      next: () => {
        this.isLoading.set(false);
        this.isSuccess.set(true);
        setTimeout(() => {
          this.router.navigate(['/dashboard']);
        }, 2000);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set('Error al crear el artículo: ' + (err.error?.detail || err.message));
      }
    });
  }
}
