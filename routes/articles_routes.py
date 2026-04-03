from fastapi import APIRouter, Depends
from core.dependences import is_redactor, get_current_user
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


# GET ARTICLES BY SECTION
@router.get("/category/{section_name}", status_code=200)
async def get_articles_by_section(section_name: str):
    return await articles_controllers.get_articles_by_section(section_name)


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

# ASSIGN CATEGORY
@router.post("/{article_id}/assign-section", status_code=200)
async def assign_section(article_id: int, section_id: int, current_user=Depends(get_current_user)):
    return await articles_controllers.assign_section(article_id, section_id, current_user)

# ELIMINAR ARTICLE
@router.delete("/{article_id}", status_code=200)
async def delete_article(article_id: str, current_user=Depends(get_current_user)):
    return await articles_controllers.delete_article(int(article_id), current_user)