import pydantic
from core.users.schemas import BlogUserModel, BlogUserUpdateModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class TagBasicModel(pydantic.BaseModel):
    name: str


class PostBasicModel(pydantic.BaseModel):
    id: int
    creator: BlogUserModel
    content: str 
    picture_url: Optional[str]
    date_created: datetime
    tags: Optional[List[TagBasicModel]]
    

class PostUpdateModel(pydantic.BaseModel):
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
    
    
class PostCreatedEvent(pydantic.BaseModel):
    event: str = 'post.created'
    id: int
    creator_id: UUID
    content: str 
    picture_url: Optional[str]
    date_created: datetime
    tags: Optional[List[TagBasicModel]]
    
    
class PostUpdatedEvent(PostCreatedEvent):
    event: str = 'post.updated'
    
    
class PostDeletedEvent(pydantic.BaseModel):
    event: str = 'post.deleted'
    post_id: int