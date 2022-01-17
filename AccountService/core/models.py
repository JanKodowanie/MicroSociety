from tortoise import fields, models
from datetime import datetime, timezone, timedelta
from common.enums import *
from tortoise.signals import pre_delete
from common.file_manager import FileManager


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
        exclude = ["password", "reset_code", "blog_user", "employee", "refresh_tokens"]
        
        
class PasswordResetCode(models.Model):
    code = fields.UUIDField(pk=True)
    user = fields.OneToOneField('models.Account', related_name='reset_code')
    exp = fields.DatetimeField(
        default=datetime.now(timezone.utc) + timedelta(hours=24))
    
    
class RefreshToken(models.Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.Account', related_name='refresh_tokens') 
    
    
@pre_delete(Account)
async def account_pre_delete(sender, instance, using_db) -> None:
    if instance.role != AccountRole.ADMINISTRATOR:
        await instance.fetch_related('blog_user')
        FileManager().delete_file(instance.blog_user.picture_path)