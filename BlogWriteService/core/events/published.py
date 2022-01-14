import pydantic
from core.posts.schemas import *
from core.comments.schemas import *


class BlogPostCreated(BlogPostGetListSchema):
    event: str = 'blog_post.created'
    
    
class BlogPostUpdated(BlogPostGetListSchema):
    event: str = 'blog_post.updated'
    
    
class BlogPostDeleted(pydantic.BaseModel):
    event: str = 'blog_post.deleted'
    post_id: str
    
    
class CommentCreated(CommentGetSchema): 
    event: str = 'comment.created'
    
    
class CommentUpdated(CommentGetSchema): 
    event: str = 'comment.updated'
    
    
class CommentDeleted(pydantic.BaseModel): 
    event: str = 'comment.deleted'
    post_id: int
    comment_id: int