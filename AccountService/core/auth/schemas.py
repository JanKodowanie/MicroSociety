import pydantic
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    
    
class PassResetCodeRequestSchema(BaseModel):
    email: pydantic.EmailStr
    
    
class PasswordResetSchema(BaseModel):
    code: UUID
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)