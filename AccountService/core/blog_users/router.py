from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Response
from .schemas import *
from .managers import *
from core.managers import AccountManager
from core.exceptions import *
from core.auth import AuthHandler
from typing import List
from uuid import UUID
from core.permissions import *
from common.responses import *
from common.enums import AccountStatus


router = APIRouter(
    tags=['Blog user'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


@router.post(
    '/blog-user', 
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
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail) 
    
    return user


@router.get(
    '/blog-user', 
    response_model=BlogUserGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_current_users_details(
    manager: BlogUserManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsBlogUser.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    return await manager.get(account.id)


@router.put(
    '/blog-user', 
    response_model=BlogUserGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def edit_current_users_details(
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
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail) 
    
    return user


@router.patch(
    '/blog-user/add-picture',
    response_model = FileUrlResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_profile_picture_for_current_user(
    picture: UploadFile = File(...),
    manager: BlogUserManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsBlogUser.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail)
    
    user = await manager.get(account.id)
    try:
        url = await manager.save_profile_picture(user, picture)
    except InvalidFileExtension as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail) 
    
    return FileUrlResponse(url=url)
    
        
@router.delete(
    '/blog-user/delete-picture',
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/blog-user/{id}', 
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
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    return user


@router.delete(
    '/blog-user/{id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_blog_user_account(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    try:
        user = await manager.get_account(id)
        if not IsModerator.has_permission(account) or not IsModerator.has_object_permission(user, account):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
        await manager.delete_account(user) 
    except AccountNotFound:
        pass
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.patch(
    '/blog-user/{id}/ban', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def ban_blog_user(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token),
    auth: AuthHandler = Depends()
):
    try:
        user = await manager.get_account(id)
        if not IsModerator.has_permission(account) or not IsModerator.has_object_permission(user, account):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
        await manager.change_users_status(user, AccountStatus.BANNED)
        await auth.perform_full_logout(user) 
    except AccountNotFound:
        pass
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.patch(
    '/blog-user/{id}/unban', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def unban_blog_user(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token),
    auth: AuthHandler = Depends()
):
    try:
        user = await manager.get_account(id)
        if not IsModerator.has_permission(account) or not IsModerator.has_object_permission(user, account):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
        await manager.change_users_status(user, AccountStatus.ACTIVE)
        await auth.perform_full_logout(user) 
    except AccountNotFound:
        pass
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.get(
    '/blog-users', 
    response_model=List[BlogUserGetListSchema],
    status_code=status.HTTP_200_OK
)
async def get_blog_users(
    manager: BlogUserManager = Depends(),
    params: ProfileListQueryParams = Depends()
):
    return await manager.get_list(params) 