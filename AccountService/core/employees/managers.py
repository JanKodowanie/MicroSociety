from .schemas import *
from .models import *
from fastapi import Depends
from common.enums import AccountRole
from core.events.event_publisher import EventPublisher
from core.managers import AccountManager
from core.exceptions import *
from core.blog_users.managers import BlogUserManager
from tortoise.exceptions import DoesNotExist
from uuid import UUID
from typing import List


class EmployeeManager:
    
    def __init__(self, broker: EventPublisher = Depends(), blog_user_manager: BlogUserManager = Depends(),
                 account_manager: AccountManager = Depends()):
        self.broker = broker
        self.blog_user_manager = blog_user_manager
        self.account_manager = account_manager
    
    async def create_admin(self, data: EmployeeCreateSchema) -> Employee:
        try:
            account = await self.account_manager.register_account(data, AccountRole.ADMINISTRATOR)
        except CredentialsAlreadyTaken as e:
            raise e
        
        employee = await Employee.create(account=account, **data.dict())
        await self.broker.publish_employee_created(employee, data.password)
        return employee
    
    async def create_moderator(self, data: EmployeeCreateSchema) -> Employee:
        try:
            blog_user = await self.blog_user_manager.create(data, AccountRole.MODERATOR)
        except CredentialsAlreadyTaken as e:
            raise e
        
        employee = await Employee.create(account=blog_user.account, **data.dict())
        await self.broker.publish_employee_created(employee, data.password)
        return employee
    
    async def get(self, id: UUID) -> Employee:
        try:
            instance = await Employee.get(account__id=id)
        except DoesNotExist:
            raise AccountNotFound()
        await instance.fetch_related('account')
        return instance
    
    async def edit(self, instance: Employee, data: EmployeeEditSchema) -> Employee:
        instance.firstname = data.firstname
        instance.lastname = data.lastname
        instance.phone_number = data.phone_number
            
        await instance.save()
        return instance
    
    async def get_list(self, params: EmployeeListQueryParams) -> List[Employee]:
        filters = params.dict()
        return await Employee.filter(**filters).prefetch_related('account')