from tortoise import fields, models
from .enums import *


class Account(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=60, unique=True)
    password = fields.CharField(max_length=128)
    bio = fields.TextField(max_length=300, null=True)
    date_joined = fields.DatetimeField(auto_now_add=True)
    points = fields.IntField(default=0)
    rank = fields.IntEnumField(enum_type=AccountRank, default=AccountRank.RANK_1)
    gender = fields.IntEnumField(enum_type=AccountGender)
    status = fields.IntEnumField(enum_type=AccountStatus, default=AccountStatus.ACTIVE)
    role = fields.IntEnumField(enum_type=AccountRole, default=AccountRole.STANDARD)
    
    
    class Meta:
        ordering = ["-date_joined"]
        
    class PydanticMeta:
        exclude = ["password"]
    
    
    '''
        do dodania:
        - picture_url
        - city
        - facebook url
        - instagram url
        
        rozważyć dodatkowe modele: Admin, Moderator
    '''