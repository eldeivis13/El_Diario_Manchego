import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException

async def get_section(section_name: str):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM sections WHERE nombre=%s", (section_name,)
            )
            section = await cursor.fetchone()
            return section
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()