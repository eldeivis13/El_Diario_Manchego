from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    mail: str
    password: str
    rol: str

# Lo que el cliente envía para registrarse
class UserCreate(BaseModel):
    nombre: str
    email: EmailStr   # valida formato de email automáticamente
    password: str
    rol: Optional[str] = "redactor"


# Lo que la API devuelve al frontend (sin contraseña)
class UserOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str

    class Config:
        from_attributes = True  


# Para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str