from typing import List
from .models import Account
from .exceptions import AccountNotFound
from utils.hash import Hash
from fastapi import Depends
from .schemas import *
from uuid import UUID
from tortoise.exceptions import DoesNotExist


class AccountManager:
    
    def __init__(self, hash: Hash = Depends()):
        self.hash = hash
        
    async def register_account(self, data: AccountCreateSchema) -> Account:
        data.password = self.hash.hash_password(data.password)    
        print(data)
        try:
            account = await Account.create(**data.dict())
        except Exception as e:
            print(e)
            
        print(account.password)
        return account
        
    async def get_account(self, uuid: UUID) -> Account:
        try:
            account = await Account.get(id=uuid)
        except DoesNotExist:
            raise AccountNotFound
        
        return account
    
    async def delete_account(self, account: Account) -> None:
        await account.delete()

    async def get_user_list(self, filters: dict) -> List[Account]:
        if not filters:
            return await Account.all()
        else:
            return await Account.filter(**filters)
        
    async def edit_account(self, account: Account, data: AccountEditSchema) -> Account:
        if data.username:
            account.username = data.username
        if data.email:
            account.email = data.email
        if data.bio:
            account.bio = data.bio
        if data.gender:
            account.gender = data.gender
            
        await account.save()            
        return account
         
    async def check_if_email_is_taken(email: str) -> bool:
        return await Account.filter(email=email).exists()
    
    async def check_if_username_is_taken(username: str) -> bool:
        return await Account.filter(username=username).exists()
            
