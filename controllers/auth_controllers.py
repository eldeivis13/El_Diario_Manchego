from fastapi import HTTPException
from db.config import get_conexion
import aiomysql as aio
from controllers.users_controllers import get_user_id
from models.user_model import UserCreate
from core.security import hash_password, verify_password, create_token

# REGISTER
async def register(user: UserCreate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            hashed_pass = hash_password(user.password)
            await cursor.execute(
                "INSERT INTO users (nombre,email,password,rol) VALUES (%s,%s,%s,%s)",
                (
                    user.nombre,
                    user.email,
                    hashed_pass,
                    user.rol,
                ),
            )
            await conn.commit()
            new_id = cursor.lastrowid
            user_db = await get_user_id(new_id)
            return {"msg": "Usuario registrado correctamente", "item": user_db}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# LOGIN
async def login(form_data):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # En OAuth2 el campo email viaja dentro de form_data.username
            await cursor.execute(
                'SELECT id, nombre, email, password, rol FROM users WHERE email = %s',
                (form_data.username,)
            )
            user = await cursor.fetchone()

            if user is None:
                raise HTTPException(status_code=404, detail="Credenciales invalidas")
            
            if not verify_password(form_data.password, user["password"]):
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
       
        token_data = {
            "id": user["id"],
            "email": user["email"],
            "nombre": user["nombre"],
            "rol": user["rol"]
        }

        token = create_token(token_data)

        # Devolver obligatoriamente access_token y token_type para que FastAPI y Swagger lo registren
        return {
            "msg": "Login correcto",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "nombre": user["nombre"],
                "email": user["email"],
                "rol": user["rol"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")