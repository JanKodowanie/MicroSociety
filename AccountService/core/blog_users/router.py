from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import *
from .managers import *
from core.accounts.exceptions import *
from core.auth.handlers import AuthHandler
from typing import List
from uuid import UUID
from core.events.event_publisher import EventPublisher


router = APIRouter(
    prefix="/blog_user",
    tags=['Blog Users']
)


@router.post(
    '/register', 
    response_model=BlogUserGetDetailsSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_blog_user(
    request: BlogUserCreateSchema, 
    manager: BlogUserManager = Depends()
    # broker: EventPublisher = Depends()
):
    try:
        user = await manager.create(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    # await broker.publish_account_created(account.id, account.username, 
    #                                      account.email, account.role)
    
    return user


@router.get(
    '/profiles', 
    response_model=List[BlogUserGetListSchema],
    status_code=status.HTTP_200_OK
)
async def get_blog_user_profile_list(
    manager: BlogUserManager = Depends()
):
    return await manager.get_list()

@router.get(
    '/profiles/{id}', 
    response_model=BlogUserGetProfileSchema,
    status_code=status.HTTP_200_OK
)
async def get_blog_user_profile(
    id: UUID, 
    manager: BlogUserManager = Depends()
):
    try:
        user = await manager.get(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    return user


# @router.get(
#     '/details', 
#     response_model=AccountOutSchema,
#     status_code=status.HTTP_200_OK
# )
# async def get_account_details(
#     account: Account = Depends(AuthHandler.get_user_from_token)
# ):
#     return account


@router.get(
    '/details/{id}', 
    response_model=BlogUserGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_account_details(
    id: UUID, 
    manager: BlogUserManager = Depends()
):
    try:
        user = await manager.get(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    return user


@router.put(
    '/details/{id}', 
    response_model=BlogUserGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def edit_account_data(
    id: UUID, 
    request: BlogUserEditSchema, 
    manager: BlogUserManager = Depends()
):
    try:
        user = await manager.get(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    
    try:
        user = await manager.edit(user, request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    return user


# @router.delete(
#     '/details', 
#     status_code=status.HTTP_204_NO_CONTENT
# )
# async def delete_account(
#     manager: AccountManager = Depends(),
#     account: Account = Depends(AuthHandler.get_user_from_token),
#     broker: EventPublisher = Depends()
# ):
#     user_id = account.id
#     await manager.delete_account(account)
#     await broker.publish_account_deleted(user_id)
#     return 