import pydantic
from pydantic import validator
from typing import Optional
from .enums import *
from .models import Account
from tortoise.contrib.pydantic import pydantic_model_creator


class AccountCreateSchema(pydantic.BaseModel):
    username: pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)
    email: pydantic.EmailStr
    # dodać szczegółową walidację
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)
    gender: AccountGender
    
    @validator('username')
    def username_is_alphanumeric(cls, value):
        if not value.isalnum():
            raise ValueError('Username must be alphanumeric')
        return value
    

class AccountEditSchema(pydantic.BaseModel):
    username: Optional[pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)]
    email: Optional[pydantic.EmailStr]
    gender: Optional[AccountGender]
    bio: Optional[pydantic.constr(strip_whitespace=True, max_length=300)]
    
    @validator('username')
    def username_is_alphanumeric(cls, value):
        if not value.isalnum():
            raise ValueError('Username must be alphanumeric')
        return value


AccountOutSchema = pydantic_model_creator(Account, name="AccountOutSchema")


class AccountListSchema(pydantic.BaseModel):
    id: pydantic.UUID4
    username: str
    rank: AccountRank
    gender: AccountGender
    status: AccountStatus
    role: AccountRole
    
    class Config:
        orm_mode = True