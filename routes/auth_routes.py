from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user_model import UserCreate
from controllers import auth_controllers 

router = APIRouter()

# registro de usuarios
@router.post('/register', status_code=201)
async def register(user: UserCreate):
    return await auth_controllers.register(user)


# login de usuarios
@router.post('/login', status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_controllers.login(form_data)