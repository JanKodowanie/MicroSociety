from common.auth.schemas import UserDataSchema
from common.enums import *
from tortoise.models import Model


class IsBlogUser:
    
    @classmethod
    def has_permission(cls, user: UserDataSchema) -> bool:
        return user.role != AccountRole.ADMINISTRATOR and user.status == AccountStatus.ACTIVE
    
    @classmethod
    def has_object_permission(cls, object: Model, user: UserDataSchema) -> bool:
        return user.role == AccountRole.MODERATOR or object.creator_id == user.sub