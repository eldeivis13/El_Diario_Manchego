import os
import aiomysql
from dotenv import load_dotenv

load_dotenv()


_pool = None

async def get_conexion():
    global _pool
    if _pool is None:
        _pool = await aiomysql.create_pool(
            host=os.getenv("MYSQL_HOST"), 
            port=int(os.getenv("MYSQL_PORT")), 
            user=os.getenv("MYSQL_USER"), 
            password=os.getenv("MYSQL_PASSWORD"),
            db=os.getenv("MYSQL_DATABASE"),
            autocommit=True,
            minsize=1, 
            maxsize=10
        )
    # create_pool devuelve un pool. acquire() nos da una conexión de ese pool.
    conn = await _pool.acquire()
    
    # Sobrescribimos el método close para que devuelva la conexión al pool
    # en lugar de destruir el socket, lo cual agota el pool rápidamente.
    conn.close = lambda: _pool.release(conn)
    
    return conn