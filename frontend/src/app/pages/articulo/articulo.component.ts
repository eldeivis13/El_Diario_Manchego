import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ArticlesService } from '../../services/articles.service';
import { AuthService } from '../../services/auth.service';
import { Article } from '../../interfaces/article.interface';

@Component({
  selector: 'app-articulo',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './articulo.component.html',
  styleUrl: './articulo.component.scss'
})
export class ArticuloComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private articlesService = inject(ArticlesService);
  public authService = inject(AuthService);

  public article = signal<Article | null>(null);
  public isLoading = signal(true);
  public error = signal<string | null>(null);
  public showDeleteModal = signal(false);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.articlesService.getArticleById(id).subscribe({
        next: (data) => {
          this.article.set(data);
          this.isLoading.set(false);
        },
        error: (err) => {
          console.error('Error fetching article', err);
          this.error.set('No se pudo cargar el artículo.');
          this.isLoading.set(false);
        }
      });
    } else {
      this.error.set('ID de artículo no válido.');
      this.isLoading.set(false);
    }
  }

  openDeleteModal(): void {
    this.showDeleteModal.set(true);
  }

  closeDeleteModal(): void {
    this.showDeleteModal.set(false);
  }

  confirmDelete(): void {
    const art = this.article();
    if (art && art.id) {
      this.articlesService.deleteArticle(art.id).subscribe({
        next: () => {
          this.closeDeleteModal();
          this.router.navigate(['/home']);
        },
        error: (err) => {
          console.error('Error al eliminar', err);
          alert('Error al intentar eliminar el artículo. ' + (err.error?.detail || err.message));
          this.closeDeleteModal();
        }
      });
    }
  }

}
