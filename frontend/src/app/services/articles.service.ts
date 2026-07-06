import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Article } from '../interfaces/article.interface';

@Injectable({
  providedIn: 'root'
})
export class ArticlesService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/articles';

  getArticles(): Observable<Article[]> {
    return this.http.get<Article[]>(`${this.apiUrl}/`);
  }

  getArticleById(id: string | number): Observable<Article> {
    return this.http.get<Article>(`${this.apiUrl}/${id}`);
  }

  updateHomeLayout(layoutBatch: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/update-layout`, layoutBatch);
  }

  getArticlesBySection(sectionName: string): Observable<Article[]> {
    return this.http.get<Article[]>(`${this.apiUrl}/category/${sectionName}`);
  }

  assignSection(articleId: number, sectionId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${articleId}/assign-section?section_id=${sectionId}`, {});
  }

  getSections(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/sections/');
  }

  createArticle(article: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/create`, article);
  }

  /**
   * Sube una imagen al servidor y devuelve la URL pública.
   * El backend espera un FormData con la clave `file`.
   */
  uploadImage(file: File): Observable<{ url: string; filename: string }> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<{ url: string; filename: string }>(
      'http://127.0.0.1:8000/media/upload-image',
      formData
    );
  }

  updateArticle(id: number, article: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, article);
  }

  deleteArticle(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  getMyArticles(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/mine`);
  }

  getArticlesInReview(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/review`);
  }

  subscribe(email: string): Observable<any> {
    return this.http.post('http://127.0.0.1:8000/subscribers/', { email });
  }

  // --- Newsletter (Editor Only) ---
  getSubscribers(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/subscribers/');
  }

  sendNewsletter(articleId: number): Observable<any> {
    return this.http.post('http://127.0.0.1:8000/subscribers/send-news', { article_id: articleId });
  }

  deleteSubscriber(id: number): Observable<any> {
    return this.http.delete(`http://127.0.0.1:8000/subscribers/${id}`);
  }

  // --- Users/Editors ---
  getEditors(): Observable<any[]> {
    return this.http.get<any[]>('http://127.0.0.1:8000/users/editors');
  }

  sendToReview(articleId: number, editorId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${articleId}/send-to-review?editor_id=${editorId}`, {});
  }
}
