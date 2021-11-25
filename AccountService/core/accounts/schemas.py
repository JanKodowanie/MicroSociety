import pydantic
from pydantic import validator
from typing import Optional
from .enums import *
from .models import Account
from .managers import AccountManager
from tortoise.contrib.pydantic import pydantic_model_creator


class AccountCreateSchema(pydantic.BaseModel):
    username: pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)
    email: pydantic.EmailStr
    # dodać szczegółową walidację
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)
    gender: AccountGender
    
    @validator('username')
    async def username_is_alphanumeric(cls, value):
        if not value.isalnum():
            raise ValueError('Username must be alphanumeric')
        return value
    
    @validator('username')
    async def username_is_taken(cls, value):
        if await AccountManager().check_if_username_is_taken(value):
            raise ValueError('Username is already taken')
        return value
        
    @validator('email')
    async def email_is_taken(cls, value):
        if await AccountManager().check_if_email_is_taken(value):
            raise ValueError('Email is already taken')
        return value


class AccountEditSchema(pydantic.BaseModel):
    username: Optional[pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)]
    email: Optional[pydantic.EmailStr]
    gender: Optional[AccountGender]
    bio: Optional[pydantic.constr(strip_whitespace=True, max_length=300)]
    
    @validator('username')
    async def username_is_alphanumeric(cls, value):
        if not value.isalnum():
            raise ValueError('Username must be alphanumeric')
        return value
    
    @validator('username')
    async def username_is_taken(cls, value):
        if await AccountManager().check_if_username_is_taken(value):
            raise ValueError('Username is already taken')
        return value
        
    @validator('email')
    async def email_is_taken(cls, value):
        if await AccountManager().check_if_email_is_taken(value):
            raise ValueError('Email is already taken')
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