from tortoise import fields, models


class FullLogoutEvent(models.Model):
    user_id = fields.UUIDField()
    logout_date = fields.DatetimeField()