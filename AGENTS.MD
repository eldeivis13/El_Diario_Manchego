# Project El diario Manchego - AI General Guidelines

Este documento centraliza las reglas generales del asistente de IA para Project El diario Manchego.

## 🤖 Rol y Perfil
Eres un experto en Python 3.14.2 con FastAPI y Angular CLI 21.2.4 enfocado en arquitectura escalable bajo MySQL 8.0.45.
Haremos especial hincapié en Angular, dado que no tenemos mucha experiencia.

## 📜 Estándares Globales

### Lenguaje y Nomenclatura
- **Español**: Nombres de variables, modelos, funciones y docstrings (formato Google) para lógica de dominio.
- **Inglés**: Keywords, nombres de librerías y términos técnicos puros.
- **Buenas Prácticas**: Aplicar en todas las tecnologías código limpio, variables claras y autoexplicativas.

### Arquitectura (Fat Models / Skinny Views)
- **Modelos/Servicios**: La lógica de negocio debe residir en modelos o capas de servicio. Mantén las funciones de controladores/vistas ligeras.

## 🛠️ Stack Tecnológico
- **Core**: Python, FastAPI
- **BD**: MySQL (usar SQL solo si es imprescindible por rendimiento).
- **Librerías y Versiones**: Consultar siempre `requirements.txt` para las dependencias del proyecto.

## 🚀 Arranque de proyecto
- `uvicorn main:app --reload` (BACKEND)
- `ng serve` (FRONTEND)

## ⚠️ Error Handling y Validación
- Usa bloques `try-except` claros en vistas (rotas/controladores) y lógica de negocio para un manejo adecuado.

## 📂 Estructura de Contexto Contextual

### BACKEND_EL-DIARIO-MANCHEGO
```
		.venv/
		controllers/
		core/
		db/
		models/
		mysql/
		routes/
	.env
	.gitignore
	main.py
	requirements.txt
```

### FRONTEND_EL-DIARIO-MANCHEGO
```
	frontend/
		.angular/
		.vscode/
		node_modules/
		public/
		src/
			app/
				components/
					footer/
					navbar/
				guards/
				interceptors/
				interfaces/
				pages/
					articulo/
					home/
					login/
					sdeportes/
					seconomia/
					spolitica/
					ssociedad/
					stecnologia/
				services/
				app.config.server.ts
				app.config.ts
				app.css
				app.html
				app.routes.server.ts
				app.routes.ts
				app.spec.ts
				app.ts
			index.html
			main.server.ts
			main.ts
			server.ts
			styles.css
		.editorconfig
		.gitignore
		angular.json
		package-lock.json
		package.json
		README.md
		tsconfig.app.json
		tsconfig.json
		tsconfig.spec.json
```
