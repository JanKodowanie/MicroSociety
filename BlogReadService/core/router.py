from fastapi import APIRouter, status, Depends
from typing import List
from .schemas import *
from .managers import *
from common.responses import *


router = APIRouter(
    tags=['Post'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


@router.get(
    '/posts',
    response_model=List[PostBasicModel]
)
async def get_post_list(
    manager: PostCollectionManager = Depends()
):
    results = await manager.get_list()
    return results