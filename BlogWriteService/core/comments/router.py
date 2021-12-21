from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import *
from .managers import *
from .exceptions import *
from core.posts.exceptions import BlogPostNotFound
from core.permissions import *
from common.auth.jwt import JWTBearer
from common.auth.schemas import UserDataSchema
from common.responses import *


router = APIRouter(
    prefix="/comments",
    tags=['Comments'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: {"detail": "Could not authenticate"},
        status.HTTP_403_FORBIDDEN: {"detail": "Not authorized"},
        status.HTTP_404_NOT_FOUND: {"detail": "Not found"}
    }
)


@router.post(
    '/{post_id}/new',
    response_model=CommentGetSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_post_comment(
    post_id: int,
    request: CommentCreateSchema,
    manager: CommentManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    if not IsBlogUser.has_permission(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    try:
        instance = await manager.create(user.sub, request, post_id)
    except BlogPostNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    
    return instance


@router.put(
    '/{comment_id}',
    status_code=status.HTTP_200_OK
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
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    
    if not IsBlogUser.has_object_permission(instance, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    return await manager.edit(instance, request)


@router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int, 
    manager: CommentManager = Depends(),
    user: UserDataSchema = Depends(JWTBearer())
):
    try:
        instance = await manager.get(comment_id)
    except CommentNotFound:
        return
    
    if not IsBlogUser.has_object_permission(instance, user) \
                and not IsModerator.has_object_permission(instance, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    await manager.delete(instance)