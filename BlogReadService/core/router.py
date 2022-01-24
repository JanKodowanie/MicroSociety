from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from .schemas import *
from .managers import *
from common.responses import *


router = APIRouter(
    tags=['Blog'],
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
    '/comment/{id}',
    response_model=CommentGetSchema
)
async def get_comment(
    id: int,
    comment_manager: CommentCollectionManager = Depends()
):
    comment = await comment_manager.get(id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie istnieje komentarz o podanym id.")
    return comment
    
    
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
    name_contains: Optional[str] = None,
    manager: TagCollectionManager = Depends()
):
    return await manager.get_tags(name_contains)