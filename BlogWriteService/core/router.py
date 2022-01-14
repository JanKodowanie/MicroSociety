from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, status, Response
from typing import List
from uuid import UUID
from core.schemas import *
from core.managers import *
from core.exceptions import *
from core.permissions import *
from typing import List
from common.auth.jwt import JWTBearer
from common.auth.schemas import UserDataSchema
from common.responses import *


router = APIRouter(
    tags=['Post'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


@router.post(
    '/post',
    response_model=PostCreatedResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_blog_post(
    content: str = Form(..., max_length=500),
    picture: UploadFile = File(None), 
    manager: PostManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    try:
        instance = await manager.create(user.sub, content, picture)
    except InvalidBlogPostData as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    
    return instance



@router.delete(
    '/post/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_blog_post(
    post_id: int, 
    manager: PostManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    try:
        instance = await manager.get(post_id)
        if not IsBlogUser.has_object_permission(instance, user) \
                and not IsModerator.has_object_permission(instance, user):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
        await manager.delete(instance)
    except PostNotFound:
        pass
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  
    

@router.patch(
    '/post/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def edit_blog_post(
    post_id: int,
    content: str = Form(None, max_length=500),
    picture: UploadFile = File(None), 
    delete_picture: bool = Form(False),
    manager: PostManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    try:
        instance = await manager.get(post_id)
    except PostNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    
    if not IsBlogUser.has_object_permission(instance, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    try:
        instance = await manager.edit(instance, content, delete_picture, picture)
    except InvalidBlogPostData as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  


@router.get(
    '/post/{post_id}',
    response_model = PostGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_blog_post(
    post_id: int,
    manager: PostManager = Depends()
):
    try:
        instance = await manager.get(post_id)
    except PostNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)

    return instance


@router.get(
    '/posts',
    response_model=List[PostGetListSchema]
)
async def get_post_list(
    manager: PostManager = Depends()
):
    return await manager.get_list()


@router.get(
    '/posts/{user_id}',
    response_model=List[PostGetListSchema]
)
async def get_posts_by_user_id(
    user_id: UUID, 
    manager: PostManager = Depends()
):
    filters = {
        "creator_id": user_id
    }
    return await manager.get_list(filters)


@router.get(
    '/tag/{name}',
    response_model=List[PostGetListSchema]
)
async def get_posts_in_tag(name: str, manager: TagManager = Depends()):
    try:
        posts = await manager.get_posts_in_tag(name)
    except TagNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NotFoundResponse().detail)
    
    return posts


@router.get(
    '/tags',
    response_model=List[TagGetFullSchema]
)
async def get_tag_list(manager: TagManager = Depends()):
    return await manager.get_tag_list()