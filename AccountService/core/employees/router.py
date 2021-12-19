from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import *
from .managers import *
from .permissions import *
from core.accounts.managers import AccountManager
from core.accounts.exceptions import *
from core.accounts.middleware import AuthHandler
from typing import List
from uuid import UUID
from core.events.event_publisher import EventPublisher
from common.responses import *


router = APIRouter(
    prefix="/employee",
    tags=['Employees']
)


@router.post(
    '/register/moderator', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_moderator(
    request: EmployeeModeratorCreateSchema, 
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token),
    broker: EventPublisher = Depends()
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    
    try:
        employee = await manager.create_moderator(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    await broker.publish_employee_created(employee, request.password)
    return employee


@router.post(
    '/register/administrator', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_administrator(
    request: EmployeeAdminCreateSchema, 
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token),
    broker: EventPublisher = Depends()
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    
    try:
        employee = await manager.create_admin(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    await broker.publish_employee_created(employee, request.password)
    return employee


@router.get(
    '/list', 
    response_model=List[EmployeeGetListSchema],
    status_code=status.HTTP_200_OK,
)
async def get_employee_list(
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    return await manager.get_list()


@router.get(
    '/details/{id}', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_employee_details(
    id: UUID, 
    manager: EmployeeManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    if not IsAdministrator.has_permission(account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    try:
        employee = await manager.get(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    return employee


@router.put(
    '/details/{id}', 
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
        raise HTTPException(404, detail=e.details)
    
    user = await manager.edit(employee, request)

    return user


@router.delete(
    '/details/{id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee(
    id: UUID, 
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    try:
        employee = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    
    if not IsAdministrator.has_permission(account) \
        or not IsAdministrator.has_object_permission(employee, account):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=ForbiddenResponse().detail) 
    
    await manager.delete_account(employee)