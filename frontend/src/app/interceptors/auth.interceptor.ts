import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // En SSR/navegador, comprobar localStorage es seguro con un chequeo
  let token = null;
  if (typeof localStorage !== 'undefined') {
    token = localStorage.getItem('manchego_token');
  }

  // Si existe el token, clonamos la request inyectando la cabecera
  if (token) {
    const clonedObj = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next(clonedObj);
  }

  // Flujo normal sin Auth
  return next(req);
};
