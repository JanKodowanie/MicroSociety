import pydantic
from typing import Optional
from common.enums import *
from core.accounts.schemas import *
from utils.validators import *


class EmployeeCreateSchema(AccountCreateSchema):
    firstname: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    lastname: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    phone_number: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)

    _firstname_is_word: classmethod = alphabetic_validator("firstname")
    _lastname_is_word: classmethod = alphabetic_validator("lastname")
    _phone_number_is_valid: classmethod = phone_number_validator("phone_number")
    
    
class EmployeeEditSchema(AccountEditSchema):
    firstname: Optional[pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)]
    lastname: Optional[pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)]
    phone_number: Optional[pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)]

    _firstname_is_word: classmethod = alphabetic_validator("firstname")
    _lastname_is_word: classmethod = alphabetic_validator("lastname")
    _phone_number_is_valid: classmethod = phone_number_validator("phone_number")
    
    
class EmployeeGetListSchema(pydantic.BaseModel):
    id: UUID
    role: AccountRole
    firstname: str
    lastname: str
    
    
class EmployeeGetDetailsSchema(EmployeeGetListSchema):
    phone_number: str
    date_joined: datetime
    email: str