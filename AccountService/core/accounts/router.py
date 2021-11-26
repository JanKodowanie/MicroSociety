from fastapi import APIRouter, Depends, HTTPException, status
from core.accounts.schemas import *
from core.accounts.exceptions import *
from core.accounts.managers import AccountManager
from core.auth.handlers import AuthHandler
from typing import List
from pydantic.types import UUID4


router = APIRouter(
    prefix="/accounts",
    tags=['Accounts']
)


@router.post(
    '/new', 
    response_model=AccountOutSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_account(request: AccountCreateSchema, manager: AccountManager = Depends()):
    try:
        account = await manager.register_account(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    return account


@router.get(
    '/list', 
    response_model=List[AccountBasicSchema],
    status_code=status.HTTP_200_OK
)
async def get_user_list(manager: AccountManager = Depends()):
    users = await manager.get_user_list()
    return users


@router.get(
    '/{id}/profile', 
    response_model=AccountOutPublicSchema,
    status_code=status.HTTP_200_OK
)
async def get_user_profile(id: UUID4, manager: AccountManager = Depends()):
    try:
        account = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    return account


@router.get(
    '/details', 
    response_model=AccountOutSchema,
    status_code=status.HTTP_200_OK
)
async def get_account_details(account: Account = Depends(AuthHandler.get_user_from_token)):
    return account


@router.put(
    '/details', 
    response_model=AccountOutSchema,
    status_code=status.HTTP_200_OK
)
async def edit_account_data(request: AccountEditSchema, manager: AccountManager = Depends(),
                        account: Account = Depends(AuthHandler.get_user_from_token)):
    try:
        account = await manager.edit_account(account, request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    return account


@router.delete(
    '/details', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_account(manager: AccountManager = Depends(),
                        account: Account = Depends(AuthHandler.get_user_from_token)):
    await manager.delete_account(account)
    return 