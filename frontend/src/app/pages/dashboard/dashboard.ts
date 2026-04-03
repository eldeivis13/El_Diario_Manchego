import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ArticlesService } from '../../services/articles.service';
import { AuthService } from '../../services/auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit {
  public articlesService = inject(ArticlesService);
  public authService = inject(AuthService);

  public myArticles = signal<any[]>([]);
  public reviewArticles = signal<any[]>([]);
  public sections = signal<any[]>([]);
  public isLoading = signal(false);

  ngOnInit(): void {
    this.loadData();
    this.loadSections();
  }

  loadData(): void {
    this.isLoading.set(true);
    if (this.authService.isRedactor()) {
      this.articlesService.getMyArticles().subscribe({
        next: (data) => {
          this.myArticles.set(data);
          this.isLoading.set(false);
        },
        error: () => this.isLoading.set(false)
      });
    } else if (this.authService.isEditor()) {
      this.articlesService.getArticlesInReview().subscribe({
        next: (data) => {
          this.reviewArticles.set(data);
          this.isLoading.set(false);
        },
        error: () => this.isLoading.set(false)
      });
    }
  }

  loadSections(): void {
    this.articlesService.getSections().subscribe(data => this.sections.set(data));
  }

  // --- Redactor Actions ---
  sendToReview(articleId: number): void {
    this.articlesService.updateArticle(articleId, { estado: 'REVISION' }).subscribe(() => {
      this.loadData();
    });
  }

  deleteArticle(articleId: number): void {
    if (confirm('¿Estás seguro de que quieres eliminar este artículo?')) {
      this.articlesService.deleteArticle(articleId).subscribe(() => {
        this.loadData();
      });
    }
  }

  // --- Editor Actions ---
  publishArticle(articleId: number, sectionId: number, importancia: number): void {
    const updateData = {
      estado: 'PUBLICADO',
      section_id: sectionId,
      importancia: importancia
    };
    this.articlesService.updateArticle(articleId, updateData).subscribe(() => {
      this.loadData();
    });
  }

  rejectArticle(articleId: number): void {
    this.articlesService.updateArticle(articleId, { estado: 'BORRADOR' }).subscribe(() => {
      this.loadData();
    });
  }
}
