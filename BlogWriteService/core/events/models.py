from tortoise import fields, models
from common.enums import *


class PublishedEvent(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=60)
    date_created = fields.DatetimeField(auto_now_add=True)
    body = fields.TextField()
    

class ReceivedEvent(models.Model):
    message_id = fields.IntField()
    date_received = fields.DatetimeField(auto_now_add=True)
    domain = fields.CharField(max_length=30)