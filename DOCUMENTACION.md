# 📰 El Diario Manchego - Documentación Técnica v1.0

## 📝 Introducción
**El Diario Manchego** es una plataforma de gestión de noticias digital diseñada para ofrecer una experiencia premium tanto a los lectores como al equipo editorial. El sistema cuenta con un flujo de trabajo jerarquizado (Redactor -> Editor) y una portada dinámica personalizable mediante arrastrar y soltar (Drag & Drop).

---

## 🛠️ Stack Tecnológico

### Backend (API REST)
- **Lenguaje:** Python 3.14.2
- **Framework:** FastAPI
- **Base de Datos:** MySQL 8.0.45
- **Driver DB:** `aiomysql` (Asíncrono)
- **Autenticación:** JWT (JSON Web Tokens)
- **Validación:** Pydantic

### Frontend (SPA)
- **Framework:** Angular CLI 21.2.4
- **Estilos:** Vanilla CSS (con arquitectura Flexbox/Grid)
- **Componentes:** Angular CDK (Drag & Drop)
- **Gestión de Estado:** Angular Signals

---

## 🏗️ Arquitectura del Sistema

### Modelos de Datos (Principales)
1.  **Users:** Gestión de perfiles con roles (`REDACTOR`, `EDITOR`).
2.  **Articles:** Corazón del sistema. Incluye campos de contenido, estado (`BORRADOR`, `REVISION`, `PUBLICADO`), metadatos de maquetación (`portada_order`, `portada_size`) y relaciones de autoría/edición.
3.  Section:** Categorías del periódico (Sociedad, Economía, Política, Deportes, Tecnología).
4.  **Subscribers:** Gestión de correos para el envío de newsletters automáticas.

### Roles y Permisos
| Característica | Lector (Público) | Redactor | Editor |
| :--- | :---: | :---: | :---: |
| Ver noticias publicadas | ✅ | ✅ | ✅ |
| Crear borradores | ❌ | ✅ | ❌ |
| Enviar a revisión | ❌ | ✅ | ❌ |
| Editar contenido | ❌ | ✅ (Solo borradores propios) | ✅ (Asignados) |
| Publicar noticias | ❌ | ❌ | ✅ |
| Eliminar noticias | ❌ | ✅ (Solo borradores) | ✅ (Cualquiera) |
| Organizar Portada (D&D) | ❌ | ❌ | ✅ |

---

## 🎨 Maquetación Dinámica (Bento Grid)

El sistema de portada permite a los **Editores** transformar el aspecto visual del periódico sin tocar una sola línea de código.

### Formatos de Tarjeta
- **Normal (1x1):** Tamaño estándar.
- **Hero (2x2):** Noticia protagonista con texto expandido y foto de gran impacto.
- **Apaisado (2x1):** Formato horizontal tipo banner con imagen y texto en paralelo.
- **Alto (1x2):** Formato vertical ideal para columnas de opinión o fotos de detalle.

### Instrucciones del Editor
1. Acceder a la Portada estando logueado como Editor.
2. Pulsar **✏️ Organizar Portada**.
3. Cambiar tamaños con los botones dedicados por tarjeta.
4. Arrastrar desde el tirador **"☰ Mover"** para reordenar la jerarquía.
5. Pulsar **💾 Guardar Layout** para hacer los cambios permanentes en la base de datos.

---

## 📧 Flujo Editorial y Newsletter

1.  **Creación:** El redactor crea un artículo. Queda en `BORRADOR`.
2.  **Revisión:** El redactor elige un editor disponible y envía la noticia. Pasa a `REVISION`.
3.  **Aprobación:** El editor asignado revisa, puede editar el contenido y finalmente cambia el estado a `PUBLICADO`.
4.  **Notificación:** Al marcar como `PUBLICADO`, el backend dispara automáticamente un proceso de **Newsletter** que notifica a todos los suscriptores de la base de datos sobre la nueva noticia.

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.14+
- Node.js 18+
- MySQL Server

### Backend
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
uvicorn main:app --reload
```

### Frontend
```bash
# Instalar dependencias
cd frontend
npm install

# Iniciar servidor de desarrollo
ng serve
```

---

## 📄 Notas de Diseño
El Diario Manchego utiliza una estética de **Modo Oscuro Premium** con efectos de *Glassmorphism* (desenfoque de cristal) y tipografías modernas (`Playfair Display` para títulos y `Inter` para lectura), optimizando la legibilidad y la retención del usuario.
