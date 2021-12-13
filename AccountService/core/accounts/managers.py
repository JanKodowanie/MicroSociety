from typing import List, Dict, Optional
from .models import *
from .exceptions import *
from .schemas import AccountCreateSchema, AccountEditSchema
from common.enums import AccountRole
from utils.hash import Hash
from uuid import UUID
from tortoise.exceptions import DoesNotExist


class AccountManager:
    
    def __init__(self):
        self.hash = Hash()
        
    async def register_account(self, data: AccountCreateSchema, 
                               role: AccountRole = AccountRole.STANDARD) -> Account:
        data.password = self.hash.hash_password(data.password)    
        
        error_fields = []
        email_taken = await self._check_if_email_is_taken(data.email)
        username_taken = await self._check_if_username_is_taken(data.username)
        
        if email_taken:
            error_fields.append('email')
        if username_taken:
            error_fields.append('username')
        
        if error_fields:
            raise CredentialsAlreadyTaken('Credentials already taken',
                    details=self._compose_credentials_taken_error(error_fields))
        
        account = await Account.create(**data.dict(), role=role)
        return account
        
    async def get_account(self, uuid: UUID) -> Account:
        try:
            account = await Account.get(id=uuid)
        except DoesNotExist:
            raise AccountNotFound()
        
        return account
    
    async def get_account_by_email(self, email: str) -> Account:
        try:
            account = await Account.get(email=email)
        except DoesNotExist:
            raise AccountNotFound()
        
        return account
    
    async def delete_account(self, account: Account) -> None:
        await account.delete()
        
    async def get_user_list(self, filters: Optional[dict] = None) -> List[Account]:
        if not filters:
            return await Account.all()
       
        return await Account.filter(**filters)
        
    async def edit_account(self, account: Account, data: AccountEditSchema) -> Account:
        error_fields = []
        if data.email and account.email != data.email:
            email_taken = await self._check_if_email_is_taken(data.email)
            if email_taken:
                error_fields.append('email')
                
        if data.username and account.username != data.username:
            username_taken = await self._check_if_username_is_taken(data.username)
            if username_taken:
                error_fields.append('username')
                
        if error_fields:
            raise CredentialsAlreadyTaken('Credentials already taken',
                    details=self._compose_credentials_taken_error(error_fields))
        
        if data.username:
            account.username = data.username
        if data.email:
            account.email = data.email
        if data.gender:
            account.gender = data.gender
            
        await account.save()            
        return account

    async def change_users_password(self, account: Account, new_password: str):
        account.password = self.hash.hash_password(new_password)
        await account.save()
        
    async def change_users_status(self, account: Account, status: AccountStatus):
        account.status = status
        await account.save()

    async def _check_if_email_is_taken(self, email: str) -> bool:
        result = await Account.filter(email=email).exists()
        return result
    
    async def _check_if_username_is_taken(self, username: str) -> bool:
        result = await Account.filter(username=username).exists()
        return result
    
    def _compose_credentials_taken_error(self, fields: List[str]):
        error_msg = []
        if 'email' in fields:
            error_msg.append('Email already taken')
        if 'username' in fields:
            error_msg.append('Username already taken')
        
        return self._compose_error_messages(fields, error_msg)
            
    def _compose_error_messages(self, field_names: List[str], messages: List[str]) -> Dict[str, str]:
        errors = {}
        
        for i in range(len(field_names)):
            errors[field_names[i]] = messages[i]
            
        return errors
    
    
class PasswordResetCodeManager:
    
    async def create_password_reset_code(self, user: Account) -> PasswordResetCode:
        await PasswordResetCode.filter(user=user).delete()
        return await PasswordResetCode.create(user=user)
    
    async def get_password_reset_code(self, code: UUID) -> PasswordResetCode:
        try:
            code = await PasswordResetCode.get(code=code).prefetch_related('user')
        except DoesNotExist:
            raise PasswordResetCodeNotFound()
        
        return code