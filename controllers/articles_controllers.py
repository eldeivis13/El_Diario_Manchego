from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.config import get_conexion
from core.dependences import get_current_user
from models.article_model import ArticleCreate, ArticleUpdate, ArticleResponse
import aiomysql
from controllers.subscribers_controllers import send_news_notification

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
                "INSERT INTO articles (titulo, contenido, estado, autor_id, fecha_publicacion, imagen_url) VALUES (%s, %s, %s, %s, %s, %s)",
                (article.title, article.content, status, user_id, fecha_pub, article.customPhotoUrl)
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al insertar en DB: {str(e)}")
    finally:
        conn.close()

    return {"msg": "Artículo creado exitosamente"}


# PUT /articles/(id) -> editar articulo

async def update_article(id: int, article: ArticleUpdate, user: dict = Depends(get_current_user)):
    try:
        conn = await get_conexion()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            # Obtener el artículo actual
            await cursor.execute(
                "SELECT autor_id, estado, editor_id FROM articles WHERE id=%s", (id,)
            )
            row = await cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Artículo no encontrado")

            es_autor = row["autor_id"] == user["id"]
            es_editor = user["rol"].lower() == "editor"
            estado_actual = row["estado"].upper()

            # Lógica de permisos restringida (Assignment-based):
            if es_editor:
                # Si el artículo ya tiene un editor asignado, solo ese editor puede meter mano.
                if row["editor_id"] is not None and row["editor_id"] != user["id"]:
                    raise HTTPException(status_code=403, detail="Este artículo está asignado a otro editor")
            else:
                # Redactor: solo si es autor Y el estado es BORRADOR.
                if not es_autor:
                    raise HTTPException(status_code=403, detail="No eres el autor de este artículo")
                if estado_actual != "BORRADOR":
                    raise HTTPException(status_code=403, detail="No puedes editar un artículo en revisión o publicado")

            # Construir la consulta dinámicamente según los campos enviados
            update_fields = []
            params = []

            if article.title is not None:
                update_fields.append("titulo = %s")
                params.append(article.title)
            
            if article.content is not None:
                update_fields.append("contenido = %s")
                params.append(article.content)

            if article.section_id is not None:
                update_fields.append("section_id = %s")
                params.append(article.section_id)

            if article.fpublicacion is not None:
                fecha = article.fpublicacion
                if "/" in fecha:
                    fecha = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S")
                update_fields.append("fecha_publicacion = %s")
                params.append(fecha)

            if article.customPhotoUrl is not None:
                update_fields.append("imagen_url = %s")
                params.append(article.customPhotoUrl)

            if article.editor_id is not None:
                update_fields.append("editor_id = %s")
                params.append(article.editor_id)

            # Solo el editor puede cambiar el estado e importancia directamente vía update (o el redactor pasando a REVISION)
            if es_editor:
                if article.estado is not None:
                    update_fields.append("estado = %s")
                    params.append(article.estado.upper())
                if article.importancia is not None:
                    update_fields.append("importancia = %s")
                    params.append(article.importancia)
            else:
                # El redactor solo puede cambiar el estado si es para enviarlo a REVISION
                if article.estado is not None and article.estado.upper() == "REVISION":
                    update_fields.append("estado = %s")
                    params.append("REVISION")

            if not update_fields:
                return {"msg": "No hay cambios que realizar"}

            params.append(id)
            query = f"UPDATE articles SET {', '.join(update_fields)} WHERE id = %s"
            
            await cursor.execute(query, tuple(params))

            # --- AUTOMATIC NEWSLETTER TRIGGER ---
            if es_editor and article.estado and article.estado.upper() == "PUBLICADO":
                # Lo lanzamos sin esperar al resultado completo para no bloquear la respuesta
                import asyncio
                asyncio.create_task(send_news_notification(id))

    finally:
        if 'conn' in locals() and conn:
            conn.close()

    return {"msg": "Artículo actualizado correctamente"}


# GET /articles 

async def get_articles():
    try:
        conn = await get_conexion()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT a.id, a.titulo, a.contenido, a.estado, a.fecha_publicacion, a.section_id, a.importancia, a.imagen_url AS customPhotoUrl, s.nombre as section_name 
                FROM articles a 
                LEFT JOIN sections s ON a.section_id = s.id
                WHERE a.estado = 'PUBLICADO'
                ORDER BY a.importancia DESC, a.fecha_publicacion DESC
                """
            )
            articles = await cursor.fetchall()
            return articles
    finally:
        if 'conn' in locals() and conn:
            conn.close()


# GET /articles/category/{nombre}

async def get_articles_by_section(nombre: str):
    try:
        conn = await get_conexion()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT a.id, a.titulo, a.contenido, a.estado, a.fecha_publicacion, a.section_id, a.imagen_url AS customPhotoUrl, s.nombre as section_name 
                FROM articles a 
                JOIN sections s ON a.section_id = s.id
                WHERE LOWER(s.nombre) = LOWER(%s)
                """, (nombre,)
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
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT a.*, a.imagen_url AS customPhotoUrl, s.nombre as section_name 
                FROM articles a 
                LEFT JOIN sections s ON a.section_id = s.id 
                WHERE a.id=%s
                """,
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

async def get_my_articles(user: dict):
    user_id = user["id"]
    try:
        conn = await get_conexion()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
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

async def send_to_review(id: int, article_status: str, editor_id: int, user: dict):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE articles SET estado=%s, editor_id=%s WHERE id=%s",
                (article_status, editor_id, id,)
            )
    finally:
        if 'conn' in locals() and conn:
            conn.close()

    return {"msg": "Artículo enviado a revisión con éxito"}

# POST /articles/assign-section

async def assign_section(id: int, section_id: int, user: dict):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE articles SET section_id=%s WHERE id=%s",
                (section_id, id,)
            )
    finally:
        if 'conn' in locals() and conn:
            conn.close()

    return {"msg": "Categoría asignada correctamente"}


# DELETE /articles/(id)

async def delete_article(id: int, user: dict):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            # Buscar artículo
            await cursor.execute("SELECT autor_id, estado FROM articles WHERE id=%s", (id,))
            row = await cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Artículo no encontrado")
                
            autor_id = row[0]
            estado = row[1]
            
            # Lógica de Permisos de roles:
            # - Si es editor: Tiene privilegios directos, puede eliminar todo.
            # - Si es redactor: Solo puede eliminar si el artículo es de su autoría y si está en BORRADOR.
            if user["rol"].lower() == "redactor":
                if autor_id != user["id"]:
                    raise HTTPException(
                        status_code=403, 
                        detail="Solo el autor o un editor pueden eliminar este artículo"
                    )
                if estado.upper() != "BORRADOR":
                    raise HTTPException(
                        status_code=403, 
                        detail="Un artículo en revisión o publicado solo puede ser eliminado por un editor"
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

# GET /articles/review -> obtener articulos en revision (SOLO LOS ASIGNADOS AL EDITOR ACTUAL)
async def get_articles_in_review(user: dict = Depends(get_current_user)):
    try:
        conn = await get_conexion()
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT a.id, a.titulo, a.contenido, a.estado, a.fecha_publicacion, a.section_id, a.importancia, a.imagen_url AS customPhotoUrl, s.nombre as section_name 
                FROM articles a 
                LEFT JOIN sections s ON a.section_id = s.id
                WHERE a.estado = 'REVISION' AND a.editor_id = %s
                ORDER BY a.fecha_publicacion DESC
                """, (user["id"],)
            )
            articles = await cursor.fetchall()
            return articles
    finally:
        if 'conn' in locals() and conn:
            conn.close()