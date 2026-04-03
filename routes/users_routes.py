from fastapi import APIRouter, Depends
from controllers import users_controllers
from models.user_model import User
from core.dependences import is_editor, is_redactor

router = APIRouter()


@router.get("/editor/{user_id}", status_code=200)
async def get_user_id_editor(user_id: str, user=Depends(is_editor)):
    return await users_controllers.get_user_id(int(user_id))

@router.get("/redactor/{user_id}", status_code=200)
async def get_user_id_redactor(user_id: str, user=Depends(is_redactor)):
    return await users_controllers.get_user_id(int(user_id))