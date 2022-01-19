import pydantic
from .models import *

   
class CommentCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, min_length=1, max_length=300)
    
    
class CommentUpdateSchema(CommentCreateSchema):
    pass    

   
class CommentCreatedResponse(pydantic.BaseModel):
    id: int
    
    class Config:
        orm_mode = True            
    

class PostCreateSchema(pydantic.BaseModel):
    content: pydantic.constr(strip_whitespace=True, min_length=1, max_length=500)
     
    
class PostCreatedResponse(pydantic.BaseModel):
    id: int
    
    class Config:
        orm_mode = True