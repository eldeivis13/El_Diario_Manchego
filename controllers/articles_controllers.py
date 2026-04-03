from fastapi import APIRouter, Depends, HTTPException
from db.config import get_conexion
from core.dependences import get_current_user
from models.article_model import ArticleCreate, ArticleUpdate, ArticleResponse
import aiomysql

router = APIRouter()

# POST /articles -> crear articulo

async def create_article(article: ArticleCreate, user: int = Depends(get_current_user)):
    user_id = user["id"]
    
    conn = await get_conexion()
    async with conn.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO articles (titulo, contenido, estado, autor_id, fecha_publicacion) VALUES (%s, %s, %s, %s, %s)",
            (article.title, article.content, article.status, user_id, article.fpublicacion)
        )

    conn.close()

    return {"msg": "Artículo creado"}


# PUT /articles/(id) -> editar articulo

async def update_article(id: int, article: ArticleUpdate, user_id: int = Depends(get_current_user)):
    conn = await get_conexion()

    async with conn.cursor() as cursor:
        # comprobar que es suyo
        await cursor.execute(
            "SELECT user_id FROM articles WHERE id=%s",
            (id,)
        )
        row = await cursor.fetchone()

        if not row or row[0] != user_id:
            raise HTTPException(status_code=403, detail="No autorizado")

        await cursor.execute(
            "UPDATE articles SET title=%s, content=%s, section=%s, fecha_publicacion=%s WHERE id=%s",
            (article.title, article.content, article.section, article.fpublicacion, id)
        )

    conn.close()

    return {"msg": "Artículo actualizado"}


# GET /articles 

async def get_articles():
    conn = await get_conexion()

    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            "SELECT titulo, contenido, estado, fecha_publicacion FROM articles"
        )
        articles = await cursor.fetchall()

    conn.close()

    return articles


# GET /articles/(id) -> obtener un article

async def get_article_by_id(id: int, user_id: int = Depends(get_current_user)):
    conn = await get_conexion()

    async with conn.cursor() as cursor:
        await cursor.execute(
            "SELECT * FROM articles WHERE id=%s",
            (id,)
        )
        article = await cursor.fetchone()

    conn.close()

    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    return article


# GET /article/mine -> mis articulos

async def get_my_articles(user_id: int = Depends(get_current_user)):
    conn = await get_conexion()

    async with conn.cursor() as cursor:
        await cursor.execute(
            "SELECT id, title, content, status FROM articles WHERE user_id=%s",
            (user_id,)
        )
        rows = await cursor.fetchall()

    conn.close()

    return rows


# POST /articles/update_status

async def send_to_review(id: int, article_status: str, user_id: int = Depends(get_current_user)):
    conn = await get_conexion()

    async with conn.cursor() as cursor:
        await cursor.execute(
            "UPDATE articles SET estado=%s WHERE id=%s",
            (article_status, id,)
        )
        row = await cursor.fetchone()

        if not row or row[0] != user_id:
            raise HTTPException(status_code=403, detail="No autorizado")

    conn.close()

    return {"msg": "Estado del articulo actualizado"}