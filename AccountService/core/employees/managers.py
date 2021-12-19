from .schemas import *
from .models import *
from fastapi import Depends
from common.enums import AccountRole
from core.events.event_publisher import EventPublisher
from core.accounts.managers import AccountManager
from core.accounts.exceptions import *
from core.blog_users.managers import BlogUserManager
from tortoise.exceptions import DoesNotExist
from uuid import UUID
from typing import List


class EmployeeManager:
    
    def __init__(self, broker: EventPublisher = Depends()):
        self.broker = broker
    
    async def create_admin(self, data: EmployeeAdminCreateSchema) -> Employee:
        try:
            account = await AccountManager().register_account(data, AccountRole.ADMINISTRATOR)
        except CredentialsAlreadyTaken as e:
            raise e
        
        employee = await Employee.create(account=account, **data.dict())
        await self.broker.publish_employee_created(employee, data.password)
        return employee
    
    async def create_moderator(self, data: EmployeeModeratorCreateSchema) -> Employee:
        try:
            blog_user = await BlogUserManager().create(data, AccountRole.MODERATOR)
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
        if data.firstname:
            instance.firstname = data.firstname
        if data.lastname:
            instance.lastname = data.lastname
        if data.phone_number:
            instance.phone_number = data.phone_number
            
        await instance.save()
        return instance
    
    async def get_list(self, filters: dict = dict()) -> List[Employee]:
        return await Employee.filter(**filters).prefetch_related('account')