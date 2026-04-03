from fastapi import APIRouter, HTTPException, Body
from controllers import subscribers_controllers
from pydantic import EmailStr, BaseModel

router = APIRouter()

class SubscriberSchema(BaseModel):
    email: EmailStr

@router.post("/", status_code=201)
async def subscribe(subscriber: SubscriberSchema):
    return await subscribers_controllers.add_subscriber(subscriber.email)
