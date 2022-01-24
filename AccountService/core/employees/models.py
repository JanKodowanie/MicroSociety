from tortoise import fields, models
from common.enums import *


class Employee(models.Model):
    account = fields.OneToOneField('models.Account')
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=30)
    phone_number = fields.CharField(max_length=9)
    fullname = fields.CharField(max_length=60, null=True)
    
    class Meta:
        ordering = ["-account__date_joined"]
        
    @classmethod
    async def create(cls, **kwargs):
        kwargs["fullname"] = " ".join([kwargs["firstname"], kwargs["lastname"]])
        return await super().create(**kwargs)