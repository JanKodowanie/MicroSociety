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
    

class BlogPostCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, min_length=1, max_length=500)
    
    
class BlogPostUpdateSchema(BlogPostCreateSchema):
    pass
    
  
class BlogPostGetListSchema(PydanticModel):
    id: int
    creator_id: UUID
    content: str 
    picture_url: Optional[str]
    date_created: datetime
    tags: Optional[List[TagGetBasicSchema]]
    
    class Config:
        orm_mode = True
    
    
class BlogPostGetDetailsSchema(BlogPostGetListSchema):
    comments: Optional[List[CommentGetSchema]]
    
    class Config:
        orm_mode = True