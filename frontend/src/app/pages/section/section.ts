import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule, SlicePipe } from '@angular/common';
import { ArticlesService } from '../../services/articles.service';
import { Article } from '../../interfaces/article.interface';
import { ActivatedRoute, RouterModule } from '@angular/router';

@Component({
  selector: 'app-section',
  standalone: true,
  imports: [CommonModule, RouterModule, SlicePipe],
  templateUrl: './section.html',
  styleUrl: './section.scss'
})
export class Section implements OnInit {
  private articlesService = inject(ArticlesService);
  private route = inject(ActivatedRoute);

  public sectionName = signal<string>('');
  public articles = signal<Article[]>([]);
  public isLoading = signal(true);

  ngOnInit(): void {
    // Subscribe to param changes so if the user clicks another category in the Navbar, it reloads seamlessly
    this.route.paramMap.subscribe(params => {
      const category = params.get('category');
      if (category) {
        this.sectionName.set(category);
        this.fetchData(category);
      }
    });
  }

  fetchData(category: string): void {
    this.isLoading.set(true);
    this.articlesService.getArticlesBySection(category).subscribe({
      next: (data) => {
        this.articles.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error fetching articles for section', err);
        this.isLoading.set(false);
      }
    });
  }
}
