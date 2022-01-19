from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from .schemas import *
from .managers import *
from common.responses import *
import settings


router = APIRouter(
    tags=['Post'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


@router.get(
    '/post/{id}',
    response_model=PostGetDetailsSchema
)
async def get_post_details(
    id: int,
    post_manager: PostCollectionManager = Depends(),
    comment_manager: CommentCollectionManager = Depends()
):
    post = await post_manager.get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie istnieje post o podanym id.")
    comments = await comment_manager.get_comments_for_post(id)
    
    return PostGetDetailsSchema(**post, comments=comments)
    
    
@router.get(
    '/posts',
    response_model=List[PostGetListSchema]
)
async def get_post_list(
    filters: PostListQueryParams = Depends(),
    manager: PostCollectionManager = Depends()
):
    return await manager.get_list(filters)


@router.get(
    '/tags',
    response_model=List[TagGetSchema]
)
async def get_tag_list(
    manager: TagCollectionManager = Depends()
):
    return await manager.get_tags()