from pydantic import BaseModel
from uuid import UUID
from common.enums import *
from typing import Optional
from datetime import datetime

        
class PasswordResetCodeCreated(BaseModel):
    event: str = 'account.password_reset'
    username: str
    email: str
    code: UUID
    
    
class FullLogout(BaseModel):
    event: str = 'account.full_logout'
    user_id: UUID
    logout_date: datetime
    
    
class BlogUserCreated(BaseModel):
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
    
    
class BlogUserDeleted(BaseModel):
    event: str = 'blog_user.deleted'
    id: UUID
    username: str
    email: str
    
    
class EmployeeCreated(BaseModel):
    event: str = 'employee.created'
    email: str
    password: str
    firstname: str
    lastname: str
    role: AccountRole