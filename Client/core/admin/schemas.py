import pydantic
from .enums import *
from common.validators import *
from common.date_converter import DateConverter
from core.accounts.enums import *
from core.accounts.schemas import AccountCreateSchema
from uuid import UUID
from typing import Optional, List


class EmployeeEditSchema(pydantic.BaseModel):
    firstname: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    lastname: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    phone_number: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    
    _firstname_is_word: classmethod = alphabetic_validator("firstname")
    _lastname_is_word: classmethod = alphabetic_validator("lastname")
    _phone_number_is_valid: classmethod = phone_number_validator("phone_number")
    
    
class EmployeeCreateSchema(AccountCreateSchema, EmployeeEditSchema):
    role: EmployeeRole

    
class EmployeeGetListSchema(pydantic.BaseModel):
    id: UUID
    role: AccountRole
    fullname: str
    phone_number: str
    
    
class EmployeeGetDetailsSchema(EmployeeGetListSchema):
    username: str
    date_joined: str
    email: str
    gender: AccountGender
    
    def dict(self, *args, **kwargs):
        employee = super().dict(*args, **kwargs)
        employee['date_joined'] = DateConverter.convert_str_to_datetime(employee['date_joined'])
        return employee 
    
    
class EmployeeListSchema(pydantic.BaseModel):
    employees: Optional[List[EmployeeGetListSchema]]
    
    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs).get('employees')