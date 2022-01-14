import pydantic
from core.users.schemas import BlogUserModel, BlogUserUpdateModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class TagBasicModel(pydantic.BaseModel):
    name: str


class BlogPostBasicModel(pydantic.BaseModel):
    id: int
    creator: BlogUserModel
    content: str 
    picture_url: Optional[str]
    date_created: datetime
    tags: Optional[List[TagBasicModel]]
    

class BlogPostUpdateModel(pydantic.BaseModel):
    content: str 
    picture_url: Optional[str]
    tags: Optional[List[TagBasicModel]]
    
    
class PostCreatorUpdateModel(BlogUserUpdateModel):
    
    def dict(self):
        return {
            "creator.username": self.username,
            "creator.gender": self.gender,
            "creator.rank": self.rank,
            "creator.picture_url": self.picture_url
        }
    
    
class BlogPostCreatedEvent(pydantic.BaseModel):
    event: str = 'blog_post.created'
    id: int
    creator_id: UUID
    content: str 
    picture_url: Optional[str]
    date_created: datetime
    tags: Optional[List[TagBasicModel]]
    
    
class BlogPostUpdatedEvent(BlogPostCreatedEvent):
    event: str = 'blog_post.updated'
    
    
class BlogPostDeletedEvent(pydantic.BaseModel):
    event: str = 'blog_post.deleted'
    post_id: int