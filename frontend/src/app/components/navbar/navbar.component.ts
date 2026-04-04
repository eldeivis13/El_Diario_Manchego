import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  public authService = inject(AuthService);
  private router = inject(Router);

  public sections = [
    { label: 'Sociedad', path: '/sociedad' },
    { label: 'Política', path: '/politica' },
    { label: 'Economía', path: '/economia' },
    { label: 'Deportes', path: '/deportes' },
    { label: 'Tecnología', path: '/tecnologia' }
  ];

  logout() {
    this.authService.logout();
    this.router.navigate(['/home']);
  }
}
