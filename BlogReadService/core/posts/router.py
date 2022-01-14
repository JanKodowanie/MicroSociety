from fastapi import APIRouter, status, Depends
from typing import List
from .schemas import *
from .managers import *


router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: {"detail": "Could not authenticate"},
        status.HTTP_403_FORBIDDEN: {"detail": "Not authorized"},
        status.HTTP_404_NOT_FOUND: {"detail": "Not found"}
    }
)


@router.get(
    '/list',
    response_model=List[BlogPostBasicModel]
)
async def get_post_list(
    manager: BlogPostCollectionManager = Depends()
):
    results = await manager.get_list()
    return results