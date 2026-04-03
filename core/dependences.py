import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from datetime import datetime, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from controllers.users_controllers import get_user_id
from core.security import decode_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 🔐 Obtener usuario actual desde el token
async def get_current_user(token: str = Depends(oauth2)):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    # ⏳ Validar expiración
    expire = payload.get("exp")
    if not expire or expire < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="Token expirado")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    # 🔎 Obtener usuario desde la base
    user = await get_user_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

async def is_redactor(user=Depends(get_current_user)):
    if user["rol"] == "redactor":
        return user

    raise HTTPException(
        status_code=403,
        detail="No eres redactor"
    )

async def is_editor(user=Depends(get_current_user)):
    if user["rol"] == "editor":
        return user

    raise HTTPException(
        status_code=403,
        detail="No eres editor"
    )