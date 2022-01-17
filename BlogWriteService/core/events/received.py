from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BlogUserDeleted(BaseModel):
    event: str = 'blog_user.deleted'
    id: UUID
    
    
class FullLogout(BaseModel):
    event: str = 'account.full_logout'
    user_id: UUID
    logout_date: datetime