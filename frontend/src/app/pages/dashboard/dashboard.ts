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

  // Custom Deletion Modal State
  public showDeleteModal = signal(false);
  public articleToDelete = signal<number | null>(null);

  ngOnInit(): void {
    this.loadData();
    this.loadSections();
  }

  loadData(): void {
    this.isLoading.set(true);
    
    // Always fetch personal articles for any logged-in user
    this.articlesService.getMyArticles().subscribe({
      next: (data) => {
        this.myArticles.set(data);
        // If not an editor, we're done loading
        if (!this.authService.isEditor()) {
          this.isLoading.set(false);
        }
      },
      error: () => {
        if (!this.authService.isEditor()) this.isLoading.set(false);
      }
    });

    // If editor, additionally fetch the review queue
    if (this.authService.isEditor()) {
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
    // Open the custom modal instead of native confirm
    this.articleToDelete.set(articleId);
    this.showDeleteModal.set(true);
  }

  confirmDelete(): void {
    const id = this.articleToDelete();
    if (id) {
      this.articlesService.deleteArticle(id).subscribe({
        next: () => {
          this.closeDeleteModal();
          this.loadData();
        },
        error: (err) => {
          alert('Error al eliminar: ' + (err.error?.detail || err.message));
          this.closeDeleteModal();
        }
      });
    }
  }

  closeDeleteModal(): void {
    this.showDeleteModal.set(false);
    this.articleToDelete.set(null);
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
