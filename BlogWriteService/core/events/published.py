import pydantic
from core.schemas import *
from core.comments.schemas import *


class PostCreated(PostGetListSchema):
    event: str = 'post.created'
    
    
class PostUpdated(PostGetListSchema):
    event: str = 'post.updated'
    
    
class PostDeleted(pydantic.BaseModel):
    event: str = 'post.deleted'
    id: str
    
    
class CommentCreated(CommentGetSchema): 
    event: str = 'comment.created'
    
    
class CommentUpdated(CommentGetSchema): 
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