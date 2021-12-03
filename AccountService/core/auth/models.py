from tortoise import fields, models
from core.accounts.models import Account
from datetime import datetime, timezone, timedelta


class PasswordResetCode(models.Model):
    code = fields.UUIDField(pk=True)
    user = fields.OneToOneField('models.Account')
    exp = fields.DatetimeField(
        default=datetime.now(timezone.utc) + timedelta(hours=24))