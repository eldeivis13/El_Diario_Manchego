import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ArticlesService } from '../../services/articles.service';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './footer.html',
  styleUrl: './footer.scss'
})
export class FooterComponent {
  private articlesService = inject(ArticlesService);
  
  email = '';
  isSubmitting = signal(false);
  message = signal<string | null>(null);

  onSubscribe(): void {
    if (!this.email) return;

    this.isSubmitting.set(true);
    this.articlesService.subscribe(this.email).subscribe({
      next: (res) => {
        this.message.set(res.msg || '¡Gracias por suscribirte!');
        this.email = '';
        this.isSubmitting.set(false);
        setTimeout(() => this.message.set(null), 5000);
      },
      error: () => {
        this.message.set('Error en la suscripción. Inténtalo de nuevo.');
        this.isSubmitting.set(false);
      }
    });
  }
}
