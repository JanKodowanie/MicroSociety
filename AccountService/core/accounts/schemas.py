import pydantic
from uuid import UUID
from typing import Optional
from common.enums import *
from utils.validators import *
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime
from .models import Account
from common.auth.schemas import *


class AccountCreateSchema(pydantic.BaseModel):
    username: pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)
    email: pydantic.EmailStr
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)
    gender: AccountGender
    
    _username_is_alphanumeric: classmethod = alphanumeric_validator("username")
    

class AccountEditSchema(pydantic.BaseModel):
    username: Optional[pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)]
    email: Optional[pydantic.EmailStr]
    gender: Optional[AccountGender]
    
    _username_is_alphanumeric: classmethod = alphanumeric_validator("username")
    
    
AccountGetDetailsSchema = pydantic_model_creator(Account, name="AccountOutSchema")


class AccountGetListSchema(pydantic.BaseModel):
    id: UUID
    username: str
    gender: AccountGender
    role: AccountRole
    status: AccountStatus
        
        
class AccountGetProfileSchema(pydantic.BaseModel):
    id: UUID
    username: str
    date_joined: datetime
    gender: AccountGender
    status: AccountStatus
    role: AccountRole
    
    
class TokenSchema(pydantic.BaseModel):
    access_token: str
    token_type: str
    data: UserDataSchema
    
    
class PassResetCodeRequestSchema(pydantic.BaseModel):
    email: pydantic.EmailStr
    
    
class PasswordResetSchema(pydantic.BaseModel):
    code: UUID
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)