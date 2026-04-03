import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ArticlesService } from '../../services/articles.service';

@Component({
  selector: 'app-editar-publicacion',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './editar-publicacion.html',
  styleUrl: './editar-publicacion.scss'
})
export class EditarPublicacionComponent implements OnInit {
  private articlesService = inject(ArticlesService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  public articleId: number | null = null;
  public title = '';
  public content = '';
  public fpublicacion = '';
  
  public isLoading = signal(true);
  public isSaving = signal(false);
  public isSuccess = signal(false);
  public errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.articleId = parseInt(id);
      this.loadArticle(this.articleId);
    } else {
      this.router.navigate(['/dashboard']);
    }
  }

  loadArticle(id: number): void {
    this.articlesService.getArticleById(id).subscribe({
      next: (article: any) => {
        this.title = article.titulo;
        this.content = article.contenido;
        this.fpublicacion = article.fecha_publicacion;
        this.isLoading.set(false);
      },
      error: (err) => {
        this.errorMessage.set('Error al cargar el artículo.');
        this.isLoading.set(false);
      }
    });
  }

  onSubmit(): void {
    if (!this.title || !this.content || !this.articleId) return;

    this.isSaving.set(true);
    this.errorMessage.set(null);

    const updateData = {
      title: this.title,
      content: this.content,
      fpublicacion: this.fpublicacion
    };

    this.articlesService.updateArticle(this.articleId, updateData).subscribe({
      next: () => {
        this.isSaving.set(false);
        this.isSuccess.set(true);
        setTimeout(() => this.router.navigate(['/dashboard']), 1500);
      },
      error: (err) => {
        this.isSaving.set(false);
        this.errorMessage.set('Error al actualizar: ' + (err.error?.detail || err.message));
      }
    });
  }
}
