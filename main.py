from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import test_db_routes, auth_routes, articles_routes, sections_routes, users_routes, subscribers_routes, upload_routes
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorio donde se guardan las imágenes subidas
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "frontend", "public", "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Servir las imágenes como ficheros estáticos en /uploads
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


@app.get("/")
def read_root():
    return {"message": "API de El Diario Manchego funcionando correctamente"}


app.include_router(test_db_routes.router, prefix="/debug", tags=["debug"])

app.include_router(auth_routes.router, prefix='/auth', tags=['auth'])

app.include_router(articles_routes.router, prefix="/articles", tags=["articles"])

app.include_router(users_routes.router, prefix="/users", tags=["users"])

app.include_router(sections_routes.router, prefix="/sections", tags=["section"])

app.include_router(subscribers_routes.router, prefix="/subscribers", tags=["subscribers"])

app.include_router(upload_routes.router, prefix="/media", tags=["media"])