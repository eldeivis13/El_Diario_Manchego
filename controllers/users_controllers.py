import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException


async def get_user_id(user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM users WHERE id=%s", (user_id,)
            )
            user = await cursor.fetchone()
            return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()