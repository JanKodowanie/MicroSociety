from .models import *
from tortoise.contrib.pydantic import pydantic_model_creator
import pydantic
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class TagSchema(pydantic.BaseModel):
    name: pydantic.constr(strip_whitespace=True, max_length=30)
    creator_id: Optional[pydantic.UUID4]
    date_created: Optional[datetime]
    
    class Config:
        orm_mode = True


class BlogPostCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, max_length=500)
    video_url: Optional[pydantic.constr(strip_whitespace=True, max_length=200)]
    image_url: Optional[pydantic.constr(strip_whitespace=True, max_length=200)]
    
    
BlogPostOutSchema = pydantic_model_creator(BlogPost, name='BlogPostOutSchema')   