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
  public imageUrl = '';
  
  public isLoading = signal(false);
  public isSuccess = signal(false);
  public errorMessage = signal<string | null>(null);

  constructor() {
    // We optionally initialize with today's date
    const today = new Date();
    this.fpublicacion = `${today.getDate().toString().padStart(2, '0')}/${(today.getMonth() + 1).toString().padStart(2, '0')}/${today.getFullYear()}`;
  }

  ngOnInit(): void {
    if (!this.authService.isRedactor()) {
      this.router.navigate(['/dashboard']);
    }
  }

  onSubmit(): void {
    if (!this.title || !this.content || !this.fpublicacion) {
      this.errorMessage.set('Por favor, completa todos los campos requeridos.');
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set(null);

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
        // After 2 seconds, redirect to our management dashboard
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
