import pydantic
from core.models import *
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class PostCreated(pydantic.BaseModel):
    event: str = 'post.created'
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
    def from_orm(cls, obj: Post) -> 'PostCreated':
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
   
    
class PostUpdated(PostCreated):
    event: str = 'post.updated'
    
    
class PostDeleted(pydantic.BaseModel):
    event: str = 'post.deleted'
    id: str
    
    
class CommentCreated(pydantic.BaseModel): 
    event: str = 'comment.created'
    id: int
    post_id: int
    content: str
    creator_id: UUID
    date_created: datetime
    
    class Config:
        orm_mode = True
    
    
class CommentUpdated(CommentCreated): 
    event: str = 'comment.updated'
    
    
class CommentDeleted(pydantic.BaseModel): 
    event: str = 'comment.deleted'
    id: int
    post_id: int
    
    
class LikeCreated(pydantic.BaseModel):
    event: str = 'like.created'
    creator_id: UUID
    post_creator_id: UUID
    post_id: int
    
    
class LikeDeleted(pydantic.BaseModel):
    event: str = 'like.deleted'
    creator_id: UUID
    post_creator_id: UUID
    post_id: int