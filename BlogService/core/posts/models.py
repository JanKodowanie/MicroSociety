from tortoise import fields, models


class Tag(models.Model):
    name = fields.CharField(max_length=30, pk=True)
    creator_id = fields.UUIDField(null=True)
    posts = fields.ManyToManyRelation["BlogPost"]
    date_created = fields.DatetimeField(auto_now_add=True)
    
    
class BlogPost(models.Model):
    post_id = fields.IntField(pk=True)
    creator_id = fields.UUIDField()
    content = fields.TextField(max_length=500)
    video_url = fields.CharField(max_length=200, null=True)
    image_url = fields.CharField(max_length=200, null=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_modified = fields.DatetimeField(auto_now=True)
    tags: fields.ManyToManyRelation["Tag"] \
        = fields.ManyToManyField(model_name='models.Tag', related_name='posts',
                    null=True)
        
    
    async def create_tags_from_content(self):
        tag_names = ['test1', 'test2', 'test3']
        for name in tag_names:
            tag = await Tag.get_or_create(name=name)
            tag = tag[0]
            if not tag.creator_id:
                tag.creator_id = self.creator_id
                await tag.save()
                
            await self.tags.add(tag)
            await self.save()