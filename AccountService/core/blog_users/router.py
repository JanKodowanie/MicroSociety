from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from .schemas import *
from .managers import *
from core.accounts.managers import AccountManager
from core.accounts.exceptions import *
from core.accounts.middleware import AuthHandler
from typing import List
from uuid import UUID
from .permissions import *
from common.responses import *
from common.enums import AccountStatus


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
):
    try:
        user = await manager.create(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details) 
    
    return user


@router.get(
    '/profiles', 
    response_model=List[BlogUserGetListSchema],
    status_code=status.HTTP_200_OK
)
async def get_blog_user_profile_list(
    manager: BlogUserManager = Depends(),
    params: ProfileListQueryParams = Depends()
):
    return await manager.get_list(params)


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
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    return user


@router.get(
    '/details', 
    response_model=BlogUserGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_account_details(
    manager: BlogUserManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsBlogUser.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    return await manager.get(account.id)


@router.put(
    '/details', 
    response_model=BlogUserGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def edit_account_data(
    request: BlogUserEditSchema, 
    manager: BlogUserManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsBlogUser.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)

    user = await manager.get(account.id)
    try:
        user = await manager.edit(user, request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details) 
    
    return user


@router.post(
    '/details/profile_picture',
    response_model = FileUrlResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_profile_picture(
    picture: UploadFile = File(...),
    manager: BlogUserManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsBlogUser.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    user = await manager.get(account.id)
    url = await manager.save_profile_picture(user, picture)
    
    return FileUrlResponse(url=url)
    
        
@router.delete(
    '/details/profile_picture', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_profile_picture(
    manager: BlogUserManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsBlogUser.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    user = await manager.get(account.id)
    await manager.delete_profile_picture(user)


@router.delete(
    '/profiles/{id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_blog_user_account(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    try:
        user = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    
    if not IsModerator.has_permission(account) or not IsModerator.has_object_permission(user, account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    
    await manager.delete_account(user) 


@router.patch(
    '/profiles/{id}/ban', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def ban_blog_user(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    try:
        user = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    
    if not IsModerator.has_permission(account) or not IsModerator.has_object_permission(user, account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    
    await manager.change_users_status(user, AccountStatus.BANNED) 


@router.patch(
    '/profiles/{id}/unban', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def unban_blog_user(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    try:
        user = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    
    if not IsModerator.has_permission(account) or not IsModerator.has_object_permission(user, account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    
    await manager.change_users_status(user, AccountStatus.ACTIVE)