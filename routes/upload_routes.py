import os
import uuid
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from core.dependences import get_current_user

router = APIRouter()

# Directorio absoluto donde se almacenan las imágenes
UPLOADS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend", "public", "uploads"
)

# URL base del servidor (configurable por variable de entorno)
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# Extensiones permitidas
EXTENSIONES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
TAMANO_MAXIMO_MB = 5


@router.post("/upload-image", status_code=201)
async def subir_imagen(
    file: UploadFile = File(...),
    usuario=Depends(get_current_user)
):
    """
    Sube una imagen al servidor y devuelve la URL pública.
    Accesible para cualquier usuario autenticado (redactores y editores).
    """
    # Validar extensión
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower()
    if ext not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no permitido. Usa: {', '.join(sorted(EXTENSIONES_PERMITIDAS))}"
        )

    # Leer contenido y validar tamaño
    contenido = await file.read()
    tamano_mb = len(contenido) / (1024 * 1024)
    if tamano_mb > TAMANO_MAXIMO_MB:
        raise HTTPException(
            status_code=400,
            detail=f"La imagen supera el límite de {TAMANO_MAXIMO_MB} MB"
        )

    # Generar nombre único para evitar colisiones
    nombre_archivo = f"{uuid.uuid4().hex}{ext}"
    ruta_destino = os.path.join(UPLOADS_DIR, nombre_archivo)

    try:
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        with open(ruta_destino, "wb") as f:
            f.write(contenido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

    # Devolver la URL pública (servida por StaticFiles en /uploads)
    url_publica = f"{BASE_URL}/uploads/{nombre_archivo}"
    return {"url": url_publica, "filename": nombre_archivo}

