from fastapi import APIRouter, HTTPException, Body, Depends
from controllers import subscribers_controllers
from pydantic import EmailStr, BaseModel
from core.dependences import is_editor

router = APIRouter()

class SubscriberSchema(BaseModel):
    email: EmailStr

@router.post("/", status_code=201)
async def subscribe(subscriber: SubscriberSchema):
    return await subscribers_controllers.add_subscriber(subscriber.email)

@router.get("/", status_code=200)
async def get_subscribers(editor=Depends(is_editor)):
    return await subscribers_controllers.get_all_subscribers()

@router.post("/send-news", status_code=200)
async def send_news_newsletter(article_id: int = Body(..., embed=True), editor=Depends(is_editor)):
    return await subscribers_controllers.send_news_notification(article_id)

@router.delete("/{id}", status_code=200)
async def remove_subscriber(id: int, editor=Depends(is_editor)):
    return await subscribers_controllers.delete_subscriber(id)
