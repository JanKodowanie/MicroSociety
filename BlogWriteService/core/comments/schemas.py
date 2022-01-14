import pydantic
from uuid import UUID
from datetime import datetime
from .models import *


class CommentCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, min_length=1, max_length=300)
    
    
class CommentUpdateSchema(CommentCreateSchema):
    pass    


class CommentGetSchema(pydantic.BaseModel):
    id: int
    post_id: int
    content: str
    creator_id: UUID
    date_created: datetime
    
    class Config:
        orm_mode = True
        
        
class CommentCreatedResponse(pydantic.BaseModel):
    id: int
    
    class Config:
        orm_mode = True        