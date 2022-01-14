import pydantic
from uuid import UUID
from common.enums import *
from typing import Optional


class BlogUserModel(pydantic.BaseModel):
    id: UUID
    username: str
    role: AccountRole
    gender: AccountGender
    rank: AccountRank
    picture_url: Optional[str]
    
    
class BlogUserUpdateModel(pydantic.BaseModel):
    username: str
    gender: AccountGender
    rank: AccountRank
    picture_url: Optional[str]
    

class BlogUserCreatedEvent(pydantic.BaseModel):
    event: str = 'blog_user.created'
    id: UUID
    username: str
    email: str
    role: AccountRole
    gender: AccountGender
    rank: AccountRank
    picture_url: Optional[str]
    
    
class BlogUserUpdatedEvent(BlogUserCreatedEvent):
    event: str = 'blog_user.updated'
    
    
class BlogUserDeletedEvent(pydantic.BaseModel):
    event: str = 'blog_user.deleted'
    id: UUID
    username: str
    email: str