import pydantic
from typing import Optional
from common.enums import *
from core.schemas import *
from .models import *
from .enums import *


class BlogUserCreateSchema(AccountCreateSchema):
    pass


class BlogUserEditSchema(BlogUserCreateSchema):
    bio: Optional[pydantic.constr(strip_whitespace=True, min_length=1, max_length=300)]
    
    
class BlogUserGetDetailsSchema(AccountGetDetailsSchema):
    bio: Optional[str]
    picture_url: Optional[str]
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
    picture_url: Optional[str]
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj: BlogUser) -> 'BlogUserGetListSchema':
        if hasattr(obj, 'account'):
            obj.id = obj.account.id
            obj.username = obj.account.username
            obj.gender = obj.account.gender
            obj.status = obj.account.status
            obj.role = obj.account.role
            
        return super().from_orm(obj)
    
    
class BlogUserGetProfileSchema(AccountGetProfileSchema):
    bio: Optional[str]
    picture_url: Optional[str]
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
    
    
class ProfileListQueryParams(pydantic.BaseModel):
    username: Optional[str]
    status: Optional[AccountStatus]
    ordering: Optional[ProfileListOrdering] = ProfileListOrdering.DATE_JOINED_DESCENDING
    
    def dict(self):
        filters_dict = {}
        if self.username:
            filters_dict['account__username__icontains'] = self.username
        if self.status:
            filters_dict['account__status'] = self.status
            
        if self.ordering == 'date_joined':
            filters_dict['ordering'] = 'account__date_joined'
        elif self.ordering == '-date_joined':
            filters_dict['ordering'] = '-account__date_joined'
        else:
            filters_dict['ordering'] = self.ordering
            
        return filters_dict