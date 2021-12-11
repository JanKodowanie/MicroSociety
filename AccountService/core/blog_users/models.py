from tortoise import fields, models
from common.enums import *


class BlogUser(models.Model):
    account = fields.OneToOneField('models.Account')
    bio = fields.TextField(max_length=300, null=True)
    points = fields.IntField(default=0)
    rank = fields.CharEnumField(enum_type=AccountRank, default=AccountRank.RANK_1)