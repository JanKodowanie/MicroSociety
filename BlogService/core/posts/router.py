from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from core.posts.schemas import *
from core.posts.managers import *
from core.posts.exceptions import *
from core.posts.permissions import *
from typing import List
from common.auth.jwt import JWTBearer
from common.auth.schemas import UserDataSchema


router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    responses= {
        401: {"detail": "Could not authenticate"},
        403: {"detail": "Not authorized"},
        404: {"detail": "Not found"}
    }
)


@router.post(
    '/new',
    response_model=BlogPostOutSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_blog_post(
    request: BlogPostCreateSchema, 
    manager: BlogPostManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(403, detail='Not authorized')
    
    instance = await manager.create_blog_post(user.sub, request)
    return instance


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_blog_post(
    id: int, 
    manager: BlogPostManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(403, detail='Not authorized')
    
    try:
        instance = await manager.get_post_by_id(id)
        if not IsBlogUser.has_object_permission(instance, user):
            raise HTTPException(403, detail='Not authorized')
    except BlogNotFound:
        return
        
    await manager.delete_blog_post(instance)


@router.get(
    '/list',
    response_model=List[BlogPostOutSchema]
)
async def get_post_list(manager: BlogPostManager = Depends()):
    return await manager.get_posts()


@router.get(
    '/list/{user_id}',
    response_model=List[BlogPostOutSchema]
)
async def get_posts_by_user_id(user_id: UUID, manager: BlogPostManager = Depends()):
    filters = {
        "user_id": user_id
    }
    return await manager.get_posts(filters)


@router.get(
    '/tags/list',
    response_model=List[TagSchema]
)
async def get_tag_list(manager: TagManager = Depends()):
    return await manager.get_tag_list()


@router.get(
    '/tags/{name}',
    response_model=List[BlogPostOutSchema]
)
async def get_posts_in_tag(name: str, manager: TagManager = Depends()):
    try:
        posts = await manager.get_posts_in_tag(name)
    except TagNotFound as e:
        raise HTTPException(404, detail=e.details)
    
    return posts