import pydantic
from .models import *
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from core.comments.schemas import CommentGetSchema
from tortoise.contrib.pydantic import PydanticModel


class TagGetBasicSchema(pydantic.BaseModel):
    name: str
    
    class Config:
        orm_mode = True


class TagGetFullSchema(TagGetBasicSchema):
    name: pydantic.constr(strip_whitespace=True, max_length=30)
    date_created: datetime
    popularity: int
    

class PostCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, min_length=1, max_length=500)
     
  
class PostGetListSchema(PydanticModel):
    id: int
    creator_id: UUID
    content: str 
    picture_url: Optional[str]
    date_created: datetime
    tag_list: Optional[List[str]]
    like_list: Optional[List[UUID]]
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj: Post) -> 'PostGetListSchema':
        if hasattr(obj, 'tags'):
            tag_list = []
            for tag in obj.tags:
                tag_list.append(tag.name)
            obj.tag_list = tag_list
            
        if hasattr(obj, 'likes'):
            like_list = []
            for like in obj.likes:
                like_list.append(like.creator_id)
            obj.like_list = like_list
            
        return super().from_orm(obj)
    
    
class PostGetDetailsSchema(PostGetListSchema):
    comments: Optional[List[CommentGetSchema]]
    
    class Config:
        orm_mode = True
        
        
class PostCreatedResponse(pydantic.BaseModel):
    id: int
    
    class Config:
        orm_mode = True