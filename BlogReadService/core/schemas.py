import pydantic
import pymongo
from core.users.schemas import BlogUserModel, BlogUserUpdateModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from .enums import *


class CommentModel(pydantic.BaseModel):
    id: int
    post_id: int
    content: str
    creator: BlogUserModel
    date_created: datetime
    
    
class CommentUpdateModel(pydantic.BaseModel):
    content: str
    
    
class CommentGetSchema(pydantic.BaseModel):
    id: int
    content: str
    creator: BlogUserModel
    date_created: datetime


class PostUpdateModel(pydantic.BaseModel):
    content: str 
    picture_url: Optional[str]
    tag_list: Optional[List[str]] = []


class PostModel(PostUpdateModel):
    id: int
    creator: BlogUserModel
    date_created: datetime
    like_list: Optional[List[UUID]] = []
    like_count: int = 0

    
class PostGetListSchema(PostModel):
    pass


class PostGetDetailsSchema(PostGetListSchema):
    comments: Optional[List[CommentGetSchema]] = []
    
    
class CreatorUpdateModel(BlogUserUpdateModel):
    
    def dict(self):
        return {
            "creator.username": self.username,
            "creator.gender": self.gender,
            "creator.rank": self.rank,
            "creator.picture_url": self.picture_url
        }
        

class TagModel(pydantic.BaseModel):
    name: str
    popularity: int = 1
    
    
class TagGetSchema(TagModel):
    pass
    
    
class PostListQueryParams(pydantic.BaseModel):
    tag: Optional[str]
    creator_id: Optional[UUID]
    ordering: Optional[PostListOrdering] = PostListOrdering.DATE_CREATED_DESCENDING
    
    def dict(self):
        filters_dict = {}
        if self.tag and self.creator_id:
            filters_dict = {"$and": [{'tag_list': self.tag}, {"creator.id": self.creator_id}]}
        elif self.tag:
            filters_dict = {'tag_list': self.tag}
        elif self.creator_id:
            filters_dict = {"creator.id": self.creator_id}
            
        if self.ordering == PostListOrdering.DATE_CREATED_DESCENDING:
            filters_dict["ordering"] = ("date_created", pymongo.DESCENDING)
        elif self.ordering == PostListOrdering.LIKE_COUNT_DESCENDING:
            filters_dict["ordering"] = ("like_count", pymongo.DESCENDING)
        return filters_dict