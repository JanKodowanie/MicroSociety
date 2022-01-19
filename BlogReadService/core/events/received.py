import pydantic
from typing import Optional, List
from common.enums import *
from uuid import UUID
from datetime import datetime

    
class ReceivedEventModel(pydantic.BaseModel):
    message_id: int
    date_received: datetime = datetime.now()
    name: str
    domain: str
    
    
class BlogUserCreated(pydantic.BaseModel):
    event: str = 'blog_user.created'
    id: UUID
    username: str
    email: str
    role: AccountRole
    gender: AccountGender
    rank: AccountRank
    picture_url: Optional[str]
    
    
class BlogUserUpdated(BlogUserCreated):
    event: str = 'blog_user.updated'
    
    
class BlogUserDeleted(pydantic.BaseModel):
    event: str = 'blog_user.deleted'
    id: UUID
    username: str
    email: str
    
    
class PostCreated(pydantic.BaseModel):
    event: str = 'post.created'
    id: int
    creator_id: UUID
    content: str 
    picture_url: Optional[str]
    date_created: datetime
    tag_list: Optional[List[str]]
    
    
class PostUpdated(PostCreated):
    event: str = 'post.updated'
    
    
class PostDeleted(pydantic.BaseModel):
    event: str = 'post.deleted'
    id: int
    
    
class CommentCreated(pydantic.BaseModel): 
    event: str = 'comment.created'
    id: int
    post_id: int
    content: str
    creator_id: UUID
    date_created: datetime
    
    
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