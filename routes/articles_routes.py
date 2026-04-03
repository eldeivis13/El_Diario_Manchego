from fastapi import APIRouter,  Depends
from core.dependences import is_redactor
from controllers import articles_controllers
from models.article_model import ArticleCreate, ArticleUpdate, ArticleResponse

router = APIRouter()


# GET ARTICLES
@router.get("/", status_code=200)
async def get_articles():
    return await articles_controllers.get_articles()


# GET MY ARTICLE
@router.get("/mine", status_code=200)
async def get_my_articles(article_id: str, user_id: str):
    return await articles_controllers.get_my_articles(article_id, user_id)


# GET ARTICLE BY ID
@router.get("/{article_id}", status_code=200)
async def get_aticles_by_id(article_id: str):
    return await articles_controllers.get_article_by_id(article_id)


# CREAR ARTICLE
@router.post('/create', status_code=201)
async def create_article(article: ArticleCreate, redactor=Depends(is_redactor)):
    return await articles_controllers.create_article(article, redactor)


# ACTUALIZAR ARTICLE
@router.put("/{article_id}", status_code=200)
async def update_article(article_id: str, article: ArticleUpdate):
    return await articles_controllers.update_article (int((article_id)), article)


# SEND TO REVIEW
@router.post("/{article_id}/send-to-review", status_code=200)
async def send_to_review(article_id: str, article: ArticleResponse, redactor=Depends(is_redactor)):
    return await articles_controllers.send_to_review(article_id, redactor, article)