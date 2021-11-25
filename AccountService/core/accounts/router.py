from fastapi import APIRouter, Depends, HTTPException, status
from core.accounts.schemas import *
from core.accounts.exceptions import *
from core.accounts.managers import AccountManager
from typing import List
from pydantic.types import UUID4


router = APIRouter(
    prefix="/accounts",
    tags=['Accounts']
)


@router.post(
    '/register', 
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
    '/get_list', 
    response_model=List[AccountListSchema],
    status_code=status.HTTP_200_OK
)
async def get_user_list(manager: AccountManager = Depends()):
    users = await manager.get_user_list()
    return users


@router.get(
    '/{id}/get_details', 
    response_model=AccountOutSchema,
    status_code=status.HTTP_200_OK
)
async def get_account_details(id: UUID4, manager: AccountManager = Depends()):
    try:
        account = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    return account


@router.put(
    '/{id}/edit', 
    response_model=AccountOutSchema,
    status_code=status.HTTP_200_OK
)
async def edit_account_data(id: UUID4, request: AccountEditSchema, manager: AccountManager = Depends()):
    try:
        account = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    # sprawdzanie uprawnień
    try:
        account = await manager.edit_account(account, request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    return account


@router.delete(
    '/{id}/delete', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_account(id: UUID4, manager: AccountManager = Depends()):
    try:
        account = await manager.get_account(id)
    except AccountNotFound as e:
        return 
    
    # sprawdzanie uprawnień
    await manager.delete_account(account)
    return 