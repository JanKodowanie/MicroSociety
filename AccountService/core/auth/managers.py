from .models import *
from .exceptions import *
from core.accounts.models import Account
from uuid import UUID
from tortoise.exceptions import DoesNotExist


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