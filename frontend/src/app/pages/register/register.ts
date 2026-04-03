import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.scss'
})
export class RegisterComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  nombre = '';
  email = '';
  password = '';
  // Redactors register themselves. Editors are usually created by admins, but we'll leave it fixed or selectable. Requirements focus on "Redactores pueden registrarse".
  rol = 'REDACTOR'; 
  
  isLoading = signal(false);
  errorMessage = signal<string | null>(null);
  successMessage = signal<string | null>(null);

  onSubmit(): void {
    if (!this.nombre || !this.email || !this.password) {
      this.errorMessage.set('Por favor, completa todos los campos.');
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set(null);

    const newUser = {
      nombre: this.nombre,
      email: this.email,
      password: this.password,
      rol: this.rol
    };

    this.authService.register(newUser).subscribe({
      next: () => {
        this.isLoading.set(false);
        this.successMessage.set('Registro exitoso. Serás redirigido al login.');
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set('Error en el registro. ' + (err.error?.detail || err.message));
      }
    });
  }
}
