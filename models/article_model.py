from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta, timezone

# Para crear artículo
class Article(BaseModel):
    itle: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    section: Optional[str] = None
    fpublicacion: Optional[str] = None

class ArticleCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    content: str = Field(min_length=10)
    status: Optional[str] = "Borrador"
    fpublicacion: str

# Para actualizar artículo
class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    editor_id: Optional[int] = None
    section: Optional[str] = None
    fpublicacion: Optional[str] = None

class UpdateStatus(BaseModel):
    status: Optional[str] = None

# Para devolver datos (response)
class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    created_at: datetime = Field(default_factory=datetime.now(tz=timezone.utc) + timedelta(hours=2))
    fpublicacion: str

    class Config:
        orm_mode = True