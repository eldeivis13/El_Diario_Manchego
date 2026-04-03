import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ArticlesService } from '../../services/articles.service';
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
  private articlesService = inject(ArticlesService);

  public article = signal<Article | null>(null);
  public isLoading = signal(true);
  public error = signal<string | null>(null);

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
}
