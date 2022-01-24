import pydantic
from settings import MEDIA_URL
from common.validators import alphanumeric_validator
from core.accounts.schemas import AccountGetBasicSchema
from typing import Optional, List
from uuid import UUID
from common.date_converter import *
from core.accounts.enums import *


class BlogUserGetBasicSchema(AccountGetBasicSchema):
    rank: AccountRank
    picture_url: Optional[str]  
    
    def dict(self, *args, **kwargs):
        user = super().dict(*args, **kwargs)
        if user['picture_url']:
            user['picture_url'] = MEDIA_URL + user['picture_url']
        return user 
    
    
class BlogUserGetProfileSchema(BlogUserGetBasicSchema):
    bio: Optional[str]
    points: int
    date_joined: str
    
    def dict(self, *args, **kwargs):
        user = super().dict(*args, **kwargs)
        user['date_joined'] = DateConverter.convert_str_to_datetime(user['date_joined'])
        return user 
    

class BlogUserGetDetailsSchema(BlogUserGetProfileSchema):
    email: str
    
    
class BlogUserListSchema(pydantic.BaseModel):
    users: Optional[List[BlogUserGetBasicSchema]]
    
    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs).get('users')
    
    
class CreatorSchema(pydantic.BaseModel):
    id: UUID
    username: str
    gender: AccountGender
    role: AccountRole
    rank: AccountRank
    picture_url: Optional[str]  
    
    def dict(self, *args, **kwargs):
        creator = super().dict(*args, **kwargs)
        if creator['picture_url']:
            creator['picture_url'] = MEDIA_URL + creator['picture_url']
        return creator 


class TagGetSchema(pydantic.BaseModel):
    name: str
    popularity: int
    
    
class TagListSchema(pydantic.BaseModel):
    tags: Optional[List[TagGetSchema]]
    
    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs).get('tags')
        
    
class CommentGetSchema(pydantic.BaseModel):
    id: int
    content: str
    creator: CreatorSchema
    date_created: str     
     
    def dict(self, *args, **kwargs):
        comment = super().dict(*args, **kwargs)
        comment['date_created'] = DateConverter.convert_str_to_datetime(comment['date_created'])
        return comment 
     
     
class PostGetListSchema(pydantic.BaseModel):
    id: int
    creator: CreatorSchema
    content: str 
    picture_url: Optional[str]
    date_created: str
    tag_list: Optional[List[str]]
    like_list: Optional[List[UUID]]
    like_count: int
    
    def dict(self, *args, **kwargs):
        post = super().dict(*args, **kwargs)
        post['date_created'] = DateConverter.convert_str_to_datetime(post['date_created'])
        if post['picture_url']:
            post['picture_url'] = MEDIA_URL + post['picture_url']
            
        return post
    

class PostGetDetailsSchema(PostGetListSchema):
    comments: Optional[List[CommentGetSchema]]
    
    
class PostListSchema(pydantic.BaseModel):
    posts: Optional[List[PostGetListSchema]]
    
    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs).get('posts')
    
    
class CreatedResponse(pydantic.BaseModel):
    id: int