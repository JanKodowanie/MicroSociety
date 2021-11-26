import uvicorn
from fastapi import FastAPI, Depends
import settings
from core.posts.schemas import *
from core.posts.managers import *
from core.posts.models import *
from typing import List


app = FastAPI()

try:
    settings.create_db_connection(app)
except Exception:
    print("Failed to create database connection")


@app.post(
    '/blogs/new',
    response_model=BlogPostOutSchema
)
async def create_blog_post(request: BlogPostCreateSchema, manager: BlogPostManager = Depends()):
    instance = await manager.create_blog_post(request)
    return instance


@app.get(
    '/blogs/list',
    response_model=List[BlogPostOutSchema]
)
async def get_post_list(manager: BlogPostManager = Depends()):
    return await manager.get_posts()


@app.get(
    '/blogs/tags/list',
    response_model=List[TagSchema]
)
async def get_tag_list():
    return await Tag.all()


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)