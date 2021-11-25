import pydantic
from typing import Optional
from .enums import AccountGender
from .models import Account
from tortoise.contrib.pydantic import pydantic_model_creator


class AccountCreateSchema(pydantic.BaseModel):
    # dodać szczegółową walidację
    username: pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)
    email: pydantic.EmailStr
    # dodać szczegółową walidację
    password: pydantic.constr(strip_whitespace=True, min_length=6, max_length=30)
    gender: AccountGender


class AccountEditSchema(pydantic.BaseModel):
    # dodać szczegółową walidację
    username: Optional[pydantic.constr(strip_whitespace=True, min_length=6, max_length=20)]
    email: Optional[pydantic.EmailStr]
    gender: Optional[AccountGender]
    bio: Optional[pydantic.constr(strip_whitespace=True, max_length=300)]


AccountOutSchema = pydantic_model_creator(Account, name="AccountOutSchema")