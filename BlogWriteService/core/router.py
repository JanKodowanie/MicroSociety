from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, status, Response
from core.schemas import *
from core.managers import *
from core.exceptions import *
from core.permissions import *
from common.auth.jwt import JWTBearer
from common.auth.schemas import AccessTokenSchema
from common.responses import *


router = APIRouter(
    tags=['Blog'],
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
    user: AccessTokenSchema = Depends(JWTBearer())
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
    user: AccessTokenSchema = Depends(JWTBearer())
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
    user: AccessTokenSchema = Depends(JWTBearer())
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


@router.post(
    '/post/{post_id}/like',
    status_code=status.HTTP_204_NO_CONTENT
)
async def create_post_like(
    post_id: int,
    manager: PostManager = Depends(),
    user: AccessTokenSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    try:
        instance = await manager.get(post_id)
    except PostNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    try:
        await manager.create_like(user.sub, instance)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.detail)

    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.delete(
    '/post/{post_id}/like',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_like(
    post_id: int,
    manager: PostManager = Depends(),
    user: AccessTokenSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    try:
        instance = await manager.get(post_id)
    except PostNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    
    await manager.delete_like(user.sub, instance)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.post(
    '/post/{post_id}/comment',
    response_model=CommentCreatedResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
    post_id: int,
    request: CommentCreateSchema,
    manager: CommentManager = Depends(),
    user: AccessTokenSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    try:
        instance = await manager.create(user.sub, request, post_id)
    except PostNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    
    return instance


@router.put(
    '/comment/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def edit_comment(
    comment_id: int, 
    request: CommentUpdateSchema,
    manager: CommentManager = Depends(),
    user: AccessTokenSchema = Depends(JWTBearer())
):
    try:
        instance = await manager.get(comment_id)
    except CommentNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    
    if not IsBlogUser.has_object_permission(instance, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    await manager.edit(instance, request)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
    

@router.delete(
    '/comment/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int, 
    manager: CommentManager = Depends(),
    user: AccessTokenSchema = Depends(JWTBearer())
):
    try:
        instance = await manager.get(comment_id)
        if not IsBlogUser.has_object_permission(instance, user) \
                and not IsModerator.has_object_permission(instance, user):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
        await manager.delete(instance)
    except CommentNotFound:
        pass
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 