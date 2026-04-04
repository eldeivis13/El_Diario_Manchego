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
  public subscribers = signal<any[]>([]);
  public sections = signal<any[]>([]);
  public editors = signal<any[]>([]);
  public isLoading = signal(false);

  // Custom Deletion Modal State
  public showDeleteModal = signal(false);
  public articleToDelete = signal<number | null>(null);

  // Custom Subscriber Deletion Modal State
  public showSubDeleteModal = signal(false);
  public subToDelete = signal<number | null>(null);

  // Assignment Modal
  public showAssignModal = signal(false);
  public articleToAssign = signal<number | null>(null);
  public selectedEditorId = 0;

  ngOnInit(): void {
    this.loadData();
    this.loadSections();
    this.loadEditors();
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

    // If editor, additionally fetch the review queue and subscribers
    if (this.authService.isEditor()) {
      this.articlesService.getArticlesInReview().subscribe({
        next: (data) => {
          this.reviewArticles.set(data);
          this.isLoading.set(false);
        },
        error: () => this.isLoading.set(false)
      });

      this.articlesService.getSubscribers().subscribe({
        next: (data) => this.subscribers.set(data),
        error: (err) => console.error('Error fetching subscribers', err)
      });
    }
  }

  loadSections(): void {
    this.articlesService.getSections().subscribe(data => this.sections.set(data));
  }

  loadEditors(): void {
    this.articlesService.getEditors().subscribe(data => this.editors.set(data));
  }

  // --- Redactor Actions ---
  sendToReview(articleId: number): void {
    // Instead of immediate action, open assignment modal
    this.articleToAssign.set(articleId);
    this.selectedEditorId = 0; // Reset
    this.showAssignModal.set(true);
  }

  confirmAssign(): void {
    const id = this.articleToAssign();
    if (id && this.selectedEditorId !== 0) {
      this.articlesService.sendToReview(id, this.selectedEditorId).subscribe(() => {
        this.closeAssignModal();
        this.loadData();
      });
    }
  }

  closeAssignModal(): void {
    this.showAssignModal.set(false);
    this.articleToAssign.set(null);
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

  // --- Newsletter Actions ---
  triggerNewsletter(articleId: number): void {
    if (confirm('¿Quieres notificar esta noticia a todos los suscriptores?')) {
      this.articlesService.sendNewsletter(articleId).subscribe({
        next: (res) => alert(res.msg),
        error: (err) => alert('Error enviando newsletter: ' + err.message)
      });
    }
  }

  removeSubscriber(id: number): void {
    // Open custom modal instead of native confirm
    this.subToDelete.set(id);
    this.showSubDeleteModal.set(true);
  }

  confirmSubDelete(): void {
    const id = this.subToDelete();
    if (id) {
      this.articlesService.deleteSubscriber(id).subscribe({
        next: () => {
          this.closeSubDeleteModal();
          this.loadData();
        },
        error: (err) => alert('Error al eliminar suscriptor: ' + err.message)
      });
    }
  }

  closeSubDeleteModal(): void {
    this.showSubDeleteModal.set(false);
    this.subToDelete.set(null);
  }
}
