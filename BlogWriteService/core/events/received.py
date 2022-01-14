from pydantic import BaseModel
from uuid import UUID


class BlogUserDeleted(BaseModel):
    event: str = 'blog_user.deleted'
    id: UUID