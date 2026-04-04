import os
import httpx
import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException

async def add_subscriber(email: str):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            # Comprobar si ya existe
            await cursor.execute("SELECT id FROM subscribers WHERE email = %s", (email,))
            if await cursor.fetchone():
                return {"msg": "Ya estás suscrito"}

            await cursor.execute(
                "INSERT INTO subscribers (email) VALUES (%s)", (email,)
            )
        return {"msg": "Suscripción exitosa"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

async def get_all_subscribers():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT id, email, fecha_alta FROM subscribers WHERE activo = 1 ORDER BY fecha_alta DESC")
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

async def delete_subscriber(subscriber_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM subscribers WHERE id = %s", (subscriber_id,))
        return {"msg": "Suscriptor eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

async def send_news_notification(article_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 1. Obtener datos de la noticia
            await cursor.execute("SELECT id, titulo, contenido FROM articles WHERE id = %s", (article_id,))
            article = await cursor.fetchone()
            if not article:
                raise HTTPException(status_code=404, detail="Noticia no encontrada")

            # 2. Obtener suscriptores
            await cursor.execute("SELECT email FROM subscribers WHERE activo = 1")
            subscribers = await cursor.fetchall()
            if not subscribers:
                return {"msg": "No hay suscriptores activos para notificar."}

            # 3. Configuración Brevo API
            api_key = os.getenv("BREVO_API_KEY")
            url = "https://api.brevo.com/v3/smtp/email"
            
            # NOTA: El remitente DEBE estar verificado en Brevo.
            sender_email = "vgonli1992@gmail.com" 

            headers = {
                "api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # 4. Enviar vía API
            async with httpx.AsyncClient() as client:
                sent_count = 0
                for sub in subscribers:
                    payload = {
                        "sender": {"name": "El Diario Manchego", "email": sender_email},
                        "to": [{"email": sub['email']}],
                        "subject": f"📰 ÚLTIMA HORA: {article['titulo']}",
                        "htmlContent": f"""
                        <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
                            <div style="max-width: 600px; margin: auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                                <h1 style="color: #e63946; border-bottom: 2px solid #e63946; padding-bottom: 10px;">El Diario Manchego</h1>
                                <h2 style="color: #1d3557;">{article['titulo']}</h2>
                                <p>Te enviamos esta notificación porque estás suscrito a nuestra newsletter regional.</p>
                                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                                <p style="font-size: 1.1rem;">Haz clic en el siguiente enlace para leer la noticia completa en nuestro portal:</p>
                                <a href="http://localhost:4200/articulo/{article['id']}" 
                                   style="display: inline-block; padding: 12px 25px; background-color: #e63946; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold;">
                                   Leer Noticia Completa
                                </a>
                                <footer style="margin-top: 30px; font-size: 0.8rem; color: #777;">
                                    &copy; 2026 El Diario Manchego - La voz de La Mancha.
                                </footer>
                            </div>
                        </body>
                        </html>
                        """
                    }
                    response = await client.post(url, headers=headers, json=payload)
                    if response.status_code == 201:
                        sent_count += 1
                        print(f"📧 API: Sent to {sub['email']}")
                    else:
                        print(f"❌ API Error sending to {sub['email']}: {response.text}")

        return {"msg": f"Newsletter enviada con éxito a {sent_count} suscriptores.", "count": sent_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en envío API: {str(e)}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
