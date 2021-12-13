from tortoise import fields, models
from common.enums import *


class Account(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=60, unique=True)
    password = fields.CharField(max_length=128)
    date_joined = fields.DatetimeField(auto_now_add=True)
    gender = fields.CharEnumField(enum_type=AccountGender)
    status = fields.CharEnumField(enum_type=AccountStatus, default=AccountStatus.ACTIVE)
    role = fields.CharEnumField(enum_type=AccountRole, default=AccountRole.STANDARD)
    
    
    class Meta:
        ordering = ["-date_joined"]
        
    class PydanticMeta:
        exclude = ["password", "reset_code", "bloguser", "employee"]