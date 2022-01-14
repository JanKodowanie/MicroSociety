import pydantic
from core.schemas import *
from core.comments.schemas import *


class PostCreated(PostGetListSchema):
    event: str = 'post.created'
    
    
class PostUpdated(PostGetListSchema):
    event: str = 'post.updated'
    
    
class PostDeleted(pydantic.BaseModel):
    event: str = 'post.deleted'
    post_id: str
    
    
class CommentCreated(CommentGetSchema): 
    event: str = 'comment.created'
    
    
class CommentUpdated(CommentGetSchema): 
    event: str = 'comment.updated'
    
    
class CommentDeleted(pydantic.BaseModel): 
    event: str = 'comment.deleted'
    post_id: int
    comment_id: int