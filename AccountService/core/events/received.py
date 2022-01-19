import pydantic
from uuid import UUID


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