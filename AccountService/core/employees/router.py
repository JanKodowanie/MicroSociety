from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import *
from .managers import *
from core.accounts.exceptions import *
from core.accounts.middleware import AuthHandler
from typing import List
from uuid import UUID
from core.events.event_publisher import EventPublisher


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
    manager: EmployeeManager = Depends()
    # broker: EventPublisher = Depends()
):
    try:
        employee = await manager.create_moderator(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    # await broker.publish_account_created(account.id, account.username, 
    #                                      account.email, account.role)
    
    return employee


@router.post(
    '/register/administrator', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_administrator(
    request: EmployeeAdminCreateSchema, 
    manager: EmployeeManager = Depends()
    # broker: EventPublisher = Depends()
):
    try:
        employee = await manager.create_admin(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    # await broker.publish_account_created(account.id, account.username, 
    #                                      account.email, account.role)
    
    return employee


@router.get(
    '/list', 
    response_model=List[EmployeeGetListSchema],
    status_code=status.HTTP_200_OK
)
async def get_employee_list(
    manager: EmployeeManager = Depends()
):
    return await manager.get_list()


@router.get(
    '/details/{id}', 
    response_model=EmployeeGetDetailsSchema,
    status_code=status.HTTP_200_OK
)
async def get_employee_details(
    id: UUID, 
    manager: EmployeeManager = Depends()
):
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
async def edit_account_data(
    id: UUID, 
    request: EmployeeEditSchema, 
    manager: EmployeeManager = Depends()
):
    try:
        employee = await manager.get(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    
    user = await manager.edit(employee, request)

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