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
        conn.close()
