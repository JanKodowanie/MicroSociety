import pydantic
from uuid import UUID
from typing import Optional
from .enums import *
from common.validators import *
from datetime import datetime


class AccountCreateSchema(pydantic.BaseModel):
    username: pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)
    email: pydantic.EmailStr
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)
    gender: AccountGender
    
    _username_is_alphanumeric: classmethod = alphanumeric_validator("username")


class BlogUserCreateSchema(AccountCreateSchema):
    pass


class BlogUserEditSchema(pydantic.BaseModel):
    username: pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)
    email: pydantic.EmailStr
    gender: AccountGender
    bio: Optional[pydantic.constr(strip_whitespace=True, min_length=1, max_length=300)]
    
    _username_is_alphanumeric: classmethod = alphanumeric_validator("username")
    

class AccountGetBasicSchema(pydantic.BaseModel):
    id: UUID
    username: str
    gender: AccountGender
    role: AccountRole
    status: AccountStatus
    

class LoginResponse(pydantic.BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    exp: datetime
    user: AccountGetBasicSchema
    
    
class LoginRequest(pydantic.BaseModel):
    username: str
    password: str
    

class PassResetCodeRequestSchema(pydantic.BaseModel):
    email: pydantic.EmailStr
    
    
class PasswordResetSchema(pydantic.BaseModel):
    code: UUID
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)
    
    def dict(self):
        return {
            "code": str(self.code),
            "password": self.password
        }
    
    
class Credentials(pydantic.BaseModel):
    access_token: str
    refresh_token: str
    exp: datetime


class UserSession(AccountGetBasicSchema):
    access_token: str