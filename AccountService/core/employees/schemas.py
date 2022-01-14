import pydantic
from common.enums import *
from core.schemas import *
from core.blog_users.schemas import BlogUserCreateSchema
from utils.validators import *
from .models import *


class EmployeeCreateSchema(BlogUserCreateSchema):
    firstname: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    lastname: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    phone_number: pydantic.constr(strip_whitespace=True, min_length=1, max_length=30)
    role: EmployeeRole

    _firstname_is_word: classmethod = alphabetic_validator("firstname")
    _lastname_is_word: classmethod = alphabetic_validator("lastname")
    _phone_number_is_valid: classmethod = phone_number_validator("phone_number")
    
    
class EmployeeEditSchema(AccountCreateSchema):
    pass
    
    
class EmployeeGetListSchema(pydantic.BaseModel):
    id: UUID
    role: AccountRole
    firstname: str
    lastname: str
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj: Employee) -> 'EmployeeGetListSchema':
        if hasattr(obj, 'account'):
            obj.id = obj.account.id
            obj.role = obj.account.role
            
        return super().from_orm(obj)
    
    
class EmployeeGetDetailsSchema(EmployeeGetListSchema):
    username: str
    phone_number: str
    date_joined: datetime
    email: str
    gender: AccountGender
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj: Employee) -> 'EmployeeGetDetailsSchema':
        if hasattr(obj, 'account'):
            obj.id = obj.account.id
            obj.username = obj.account.username
            obj.email = obj.account.email
            obj.date_joined = obj.account.date_joined
            obj.gender = obj.account.gender
            obj.role = obj.account.role
            
        return super().from_orm(obj)