from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, status
from typing import List
from uuid import UUID
from core.posts.schemas import *
from core.posts.managers import *
from core.posts.exceptions import *
from core.permissions import *
from typing import List
from common.auth.jwt import JWTBearer
from common.auth.schemas import UserDataSchema
from common.responses import *


router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: {"detail": "Could not authenticate"},
        status.HTTP_403_FORBIDDEN: {"detail": "Not authorized"},
        status.HTTP_404_NOT_FOUND: {"detail": "Not found"}
    }
)


@router.post(
    '/new',
    response_model=BlogPostGetDetailsSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_blog_post(
    content: str = Form(..., max_length=500),
    picture: UploadFile = File(None), 
    manager: BlogPostManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    print(picture)
    
    try:
        instance = await manager.create(user.sub, content, picture)
    except InvalidBlogPostData as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    
    return instance


@router.get(
    '/list',
    response_model=List[BlogPostGetListSchema]
)
async def get_post_list(
    manager: BlogPostManager = Depends()
):
    return await manager.get_list()


@router.get(
    '/list/{user_id}',
    response_model=List[BlogPostGetListSchema]
)
async def get_posts_by_user_id(
    user_id: UUID, 
    manager: BlogPostManager = Depends()
):
    filters = {
        "creator_id": user_id
    }
    return await manager.get_list(filters)


@router.get(
    '/{id}',
    response_model = BlogPostGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_blog_post(
    id: int,
    manager: BlogPostManager = Depends()
):
    try:
        instance = await manager.get(id)
    except BlogNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NotFoundResponse().detail)

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
    try:
        instance = await manager.get(id)
    except BlogNotFound:
        return
    
    if not IsBlogUser.has_object_permission(instance, user) \
                and not IsModerator.has_object_permission(instance, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    await manager.delete(instance)
    
    
@router.put(
    '/{id}',
    response_model = BlogPostGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def edit_blog_post(
    id: int,
    content: str = Form(None, max_length=500),
    picture: UploadFile = File(None), 
    delete_picture: bool = Form(False),
    manager: BlogPostManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    try:
        instance = await manager.get(id)
    except BlogNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NotFoundResponse().detail)
    
    if not IsBlogUser.has_object_permission(instance, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    try:
        instance = await manager.edit(instance, content, delete_picture, picture)
    except InvalidBlogPostData as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    
    return instance


@router.get(
    '/tags/list',
    response_model=List[TagGetFullSchema]
)
async def get_tag_list(manager: TagManager = Depends()):
    return await manager.get_tag_list()


@router.get(
    '/tags/{name}',
    response_model=List[BlogPostGetListSchema]
)
async def get_posts_in_tag(name: str, manager: TagManager = Depends()):
    try:
        posts = await manager.get_posts_in_tag(name)
    except TagNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NotFoundResponse().detail)
    
    return posts