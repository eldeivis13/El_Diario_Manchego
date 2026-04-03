import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ArticuloComponent } from './pages/articulo/articulo.component';
import { Section } from './pages/section/section';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'articulo/:id', component: ArticuloComponent },
  { path: ':category', component: Section }
];
