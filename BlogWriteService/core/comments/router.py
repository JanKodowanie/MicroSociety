from fastapi import APIRouter, Depends, HTTPException, status, Response
from .schemas import *
from .managers import *
from .exceptions import *
from core.exceptions import PostNotFound
from core.permissions import *
from common.auth.jwt import JWTBearer
from common.auth.schemas import UserDataSchema
from common.responses import *


router = APIRouter(
    tags=['Comment'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


@router.post(
    '/post/{post_id}/comment',
    response_model=CommentCreatedResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
    post_id: int,
    request: CommentCreateSchema,
    manager: CommentManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
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
    user: UserDataSchema = Depends(JWTBearer())
):
    try:
        instance = await manager.get(comment_id)
    except CommentNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    
    if not IsBlogUser.has_object_permission(instance, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    await manager.edit(instance, request)
    

@router.delete(
    '/comment/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int, 
    manager: CommentManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
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