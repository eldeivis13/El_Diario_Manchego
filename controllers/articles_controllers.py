from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.config import get_conexion
from core.dependences import get_current_user
from models.article_model import ArticleCreate, ArticleUpdate, ArticleResponse
import aiomysql

router = APIRouter()

# POST /articles -> crear articulo

async def create_article(article: ArticleCreate, user: dict):
    user_id = user["id"]
    
    status = article.status.upper() if article.status else "BORRADOR"
    
    fecha_pub = article.fpublicacion
    try:
        if "/" in fecha_pub:
            fecha_pub = datetime.strptime(fecha_pub, "%d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        pass
        
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO articles (titulo, contenido, estado, autor_id, fecha_publicacion) VALUES (%s, %s, %s, %s, %s)",
                (article.title, article.content, status, user_id, fecha_pub)
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al insertar en DB: {str(e)}")
    finally:
        conn.close()

    return {"msg": "Artículo creado exitosamente"}


# PUT /articles/(id) -> editar articulo

async def update_article(id: int, article: ArticleUpdate, user_id: int = Depends(get_current_user)):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            # comprobar que es suyo
            await cursor.execute(
                "SELECT autor_id FROM articles WHERE id=%s",
                (id,)
            )
            row = await cursor.fetchone()

            if not row or row[0] != user_id:
                raise HTTPException(status_code=403, detail="No autorizado")

            await cursor.execute(
                "UPDATE articles SET titulo=%s, contenido=%s, section_id=%s, fecha_publicacion=%s WHERE id=%s",
                (article.title, article.content, article.section, article.fpublicacion, id)
            )
    finally:
        if 'conn' in locals() and conn:
            conn.close()

    return {"msg": "Artículo actualizado"}


# GET /articles 

async def get_articles():
    try:
        conn = await get_conexion()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT titulo, contenido, estado, fecha_publicacion FROM articles"
            )
            articles = await cursor.fetchall()
            return articles
    finally:
        if 'conn' in locals() and conn:
            conn.close()


# GET /articles/(id) -> obtener un article

async def get_article_by_id(id: int, user_id: int = Depends(get_current_user)):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM articles WHERE id=%s",
                (id,)
            )
            article = await cursor.fetchone()
            
        if not article:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")
        return article
    finally:
        if 'conn' in locals() and conn:
            conn.close()


# GET /article/mine -> mis articulos

async def get_my_articles(user_id: int = Depends(get_current_user)):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, titulo, contenido, estado FROM articles WHERE autor_id=%s",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return rows
    finally:
        if 'conn' in locals() and conn:
            conn.close()


# POST /articles/update_status

async def send_to_review(id: int, article_status: str, user: dict):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE articles SET estado=%s WHERE id=%s",
                (article_status, id,)
            )
            # Fetching after update without SELECT doesn't work this way in MySQL but we won't crash it if it's there.
    finally:
        if 'conn' in locals() and conn:
            conn.close()

    return {"msg": "Estado del articulo actualizado"}


# DELETE /articles/(id)

async def delete_article(id: int, user: dict):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            # Buscar artículo
            await cursor.execute("SELECT autor_id FROM articles WHERE id=%s", (id,))
            row = await cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Artículo no encontrado")
                
            autor_id = row[0]
            
            # Lógica de Permisos de roles:
            # - Si es editor: Tiene privilegios directos, puede eliminar todo.
            # - Si es redactor: Solo puede eliminar si el artículo es de su autoría.
            if user["rol"].lower() == "redactor" and autor_id != user["id"]:
                raise HTTPException(
                    status_code=403, 
                    detail="Solo el autor o un editor pueden eliminar este artículo"
                )
            
            # Proceder a eliminar
            await cursor.execute("DELETE FROM articles WHERE id=%s", (id,))
            
        return {"msg": "Artículo eliminado correctamente"}
    except HTTPException:
        # Re-raise HTTP exceptions to not mask them 
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error borrando de base de datos: {str(e)}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()