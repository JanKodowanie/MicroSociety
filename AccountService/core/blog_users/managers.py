from .schemas import *
from .models import *
from common.enums import AccountRole
from core.accounts.managers import AccountManager
from core.accounts.exceptions import *
from tortoise.exceptions import DoesNotExist
from uuid import UUID
from typing import List


class BlogUserManager:
    
    async def create(self, data: BlogUserCreateSchema, role: AccountRole = AccountRole.STANDARD) -> BlogUser:
        try:
            account = await AccountManager().register_account(data, role)
        except CredentialsAlreadyTaken as e:
            raise e
        
        return await BlogUser.create(account=account, **data.dict())
    
    async def get(self, id: UUID) -> BlogUser:
        try:
            instance = await BlogUser.get(account__id=id)
        except DoesNotExist:
            raise AccountNotFound()
        await instance.fetch_related('account')
        return instance
    
    async def edit(self, instance: BlogUser, data: BlogUserEditSchema) -> BlogUser:
        try:
            await AccountManager().edit_account(instance.account, data)
        except CredentialsAlreadyTaken as e:
            raise e
        
        if data.bio:
            instance.bio = data.bio
            
        await instance.save()
        return instance
    
    async def get_list(self, filters: dict = dict()) -> List[BlogUser]:
        return await BlogUser.filter(**filters).prefetch_related('account')