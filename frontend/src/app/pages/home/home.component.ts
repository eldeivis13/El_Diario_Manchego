import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ArticlesService } from '../../services/articles.service';
import { AuthService } from '../../services/auth.service';
import { Article } from '../../interfaces/article.interface';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  private articlesService = inject(ArticlesService);
  public authService = inject(AuthService); // Public for HTML access
  
  public articles = signal<Article[]>([]);
  public sections = signal<any[]>([]);
  public isLoading = signal(true);
  
  // Temporary state dict to hold selected section id per article in the UI list
  public selectedSections: { [articleId: number]: number } = {};

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.isLoading.set(true);
    // Fetch articles
    this.articlesService.getArticles().subscribe({
      next: (data) => {
        this.articles.set(data);
        // Initialize dropdowns locally 
        data.forEach(a => { if (a.id) this.selectedSections[a.id] = a.section_id || 0; });
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error fetching articles', err);
        this.isLoading.set(false);
      }
    });

    // Fetch sections for the editor tool
    this.articlesService.getSections().subscribe({
      next: (data) => this.sections.set(data),
      error: (err) => console.error('Error fetching sections', err)
    });
  }

  assignSection(articleId: number | undefined): void {
    if (!articleId) return;
    const sectionId = this.selectedSections[articleId];
    if (!sectionId || sectionId === 0) return;

    this.articlesService.assignSection(articleId, sectionId).subscribe({
      next: () => {
        alert('Categoría asignada correctamente');
        // Update local state without full reload
        const currentArticles = this.articles();
        const sectionName = this.sections().find(s => s.id == sectionId)?.nombre;
        this.articles.set(currentArticles.map(a => 
          a.id === articleId ? { ...a, section_id: sectionId, section_name: sectionName } : a
        ));
      },
      error: (err) => alert('Error al asignar categoría: ' + err.message)
    });
  }
}
