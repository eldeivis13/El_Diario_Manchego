from fastapi import APIRouter
from models.user_model import UserCreate, UserLogin
from controllers import auth_controllers 

router = APIRouter()

# registro de usuarios


# inserción de un usuario en la base de datos /auth/register
@router.post('/register', status_code=201)
async def register(user: UserCreate):
    return await auth_controllers.register(user)


# login de usuarios
@router.post('/login', status_code=200)
async def login(user_login: UserLogin):
    return await auth_controllers.login(user_login)