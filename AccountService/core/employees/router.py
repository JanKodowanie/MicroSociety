from fastapi import APIRouter, Depends, HTTPException, status, Response
from .schemas import *
from .managers import *
from core.permissions import *
from core.managers import AccountManager
from core.exceptions import *
from core.auth import AuthHandler
from typing import List
from uuid import UUID
from common.responses import *
from common.enums import EmployeeRole


router = APIRouter(
    tags=['Employee'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


@router.post(
    '/employee', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_employee(
    request: EmployeeCreateSchema, 
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    
    try:
        if request.role == EmployeeRole.MODERATOR:
            employee = await manager.create_moderator(request)
        else:
            employee = await manager.create_admin(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail) 
    
    return employee


@router.get(
    '/employees', 
    response_model=List[EmployeeGetListSchema],
    status_code=status.HTTP_200_OK,
)
async def get_employees(
    params: EmployeeListQueryParams = Depends(),
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    return await manager.get_list(params)


@router.get(
    '/employee/{id}', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_employee(
    id: UUID, 
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    try:
        employee = await manager.get(id)
    except AccountNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    
    return employee


@router.put(
    '/employee/{id}', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def edit_employee_data(
    id: UUID, 
    request: EmployeeEditSchema, 
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    try:
        employee = await manager.get(id)
    except AccountNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)
    
    user = await manager.edit(employee, request)
    return user


@router.delete(
    '/employee/{id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    try:
        employee = await manager.get_account(id)
        if not IsAdministrator.has_permission(account) \
            or not IsAdministrator.has_object_permission(employee, account):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
        await manager.delete_account(employee)
    except AccountNotFound as e:
        pass
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 