from fastapi import APIRouter, Depends
from controllers import sections_controllers
from models.user_model import User
from core.dependences import is_editor

router = APIRouter()


@router.get("/", status_code=200)
async def get_all_sections(user=Depends(is_editor)):
    return await sections_controllers.get_all_sections()

@router.get("/{section_name}", status_code=200)
async def get_section(section_name: str, user=Depends(is_editor)):
    return await sections_controllers.get_section(str(section_name))