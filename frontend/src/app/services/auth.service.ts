import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface User {
  id: number;
  nombre: string;
  email: string;
  rol: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000';
  
  // Reactively store the current user for UI updates
  public currentUser = signal<User | null>(null);

  constructor() {
    this.checkToken();
  }

  checkToken(): void {
    // Hydrate state from localStorage immediately on startup
    if (typeof localStorage !== 'undefined') {
      const storedUser = localStorage.getItem('manchego_user');
      if (storedUser) {
        try {
          this.currentUser.set(JSON.parse(storedUser));
        } catch (e) {
          console.error("Failed to parse stored user", e);
        }
      }
    }
  }

  login(username: string, password: string): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });
    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);

    return this.http.post<any>(`${this.apiUrl}/auth/login`, body.toString(), { headers }).pipe(
      tap(response => {
        if (response.access_token && typeof localStorage !== 'undefined') {
          localStorage.setItem('manchego_token', response.access_token);
          localStorage.setItem('manchego_user', JSON.stringify(response.user));
          this.currentUser.set(response.user);
        }
      })
    );
  }

  logout(): void {
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('manchego_token');
      localStorage.removeItem('manchego_user');
    }
    this.currentUser.set(null);
  }

  isEditor(): boolean {
    const user = this.currentUser();
    return user !== null && user.rol.toUpperCase() === 'EDITOR';
  }
}
