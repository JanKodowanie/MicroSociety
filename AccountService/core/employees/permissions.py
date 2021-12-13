from common.enums import *
from tortoise.models import Model
from core.accounts.models import Account

        
class IsAdministrator:
    
    @classmethod
    def has_permission(cls, user: Account) -> bool:
        return user.role == AccountRole.ADMINISTRATOR
    
    @classmethod
    def has_object_permission(cls, object: Model, user: Account) -> bool:
        return object.role != AccountRole.STANDARD and object.id != user.id