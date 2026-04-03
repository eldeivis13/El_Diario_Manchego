import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ArticuloComponent } from './pages/articulo/articulo.component';
import { Section } from './pages/section/section';
import { LoginComponent } from './pages/login/login.component';
import { NuevaPublicacionComponent } from './pages/nueva-publicacion/nueva-publicacion';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'nueva-publicacion', component: NuevaPublicacionComponent },
  { path: 'articulo/:id', component: ArticuloComponent },
  { path: ':category', component: Section }
];
