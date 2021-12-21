from tortoise import fields, models


class Comment(models.Model):
    creator_id = fields.UUIDField()
    post = fields.ForeignKeyField(model_name="models.BlogPost", related_name="comments")
    content = fields.TextField(max_length=300)
    date_created = fields.DatetimeField(auto_now_add=True)
        
    class Meta:
        ordering = ["date_created"]