import pydantic
from settings import MEDIA_URL, logger
from fastapi import UploadFile
from core.accounts.schemas import BlogUserGetBasicSchema
from typing import Optional, List
from uuid import UUID
from common.date_converter import *
from core.accounts.enums import *


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
    
    
class PostCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, min_length=1, max_length=500)
    picture: Optional[UploadFile]
    
    
class CommentCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, min_length=1, max_length=300)     
    
    
class CommentGetSchema(pydantic.BaseModel):
    id: int
    content: str
    creator: CreatorSchema
    date_created: datetime     
     
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