import pydantic
from typing import Optional
from common.enums import *
from core.accounts.schemas import *
from .models import *


class BlogUserCreateSchema(AccountCreateSchema):
    pass


class BlogUserEditSchema(AccountEditSchema):
    bio: Optional[pydantic.constr(strip_whitespace=True, min_length=1, max_length=300)]
    
    
class BlogUserGetDetailsSchema(AccountGetDetailsSchema):
    bio: Optional[str]
    points: int
    rank: AccountRank
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj: BlogUser) -> 'BlogUserGetDetailsSchema':
        if hasattr(obj, 'account'):
            obj.id = obj.account.id
            obj.username = obj.account.username
            obj.email = obj.account.email
            obj.date_joined = obj.account.date_joined
            obj.gender = obj.account.gender
            obj.status = obj.account.status
            obj.role = obj.account.role
            
        return super().from_orm(obj)
        
    
class BlogUserGetListSchema(AccountGetListSchema):
    rank: AccountRank
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj: BlogUser) -> 'BlogUserGetListSchema':
        if hasattr(obj, 'account'):
            obj.id = obj.account.id
            obj.username = obj.account.username
            obj.gender = obj.account.gender
            obj.role = obj.account.role
            
        return super().from_orm(obj)
    
    
class BlogUserGetProfileSchema(AccountGetProfileSchema):
    bio: Optional[str]
    points: int
    rank: AccountRank
    
    class Config:
        orm_mode = True
    
    @classmethod
    def from_orm(cls, obj: BlogUser) -> 'BlogUserGetProfileSchema':
        if hasattr(obj, 'account'):
            obj.id = obj.account.id
            obj.username = obj.account.username
            obj.date_joined = obj.account.date_joined
            obj.gender = obj.account.gender
            obj.status = obj.account.status
            obj.role = obj.account.role
            
        return super().from_orm(obj)