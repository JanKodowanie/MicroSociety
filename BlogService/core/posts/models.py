from tortoise import fields, models
from typing import List
import re


class Tag(models.Model):
    name = fields.CharField(max_length=30, pk=True)
    creator_id = fields.UUIDField(null=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    posts: fields.ManyToManyRelation["BlogPost"]
    
    
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
        
        
    class Meta:
        ordering = ["-date_created"]
        
        
    async def create_tags_from_content(self) -> None:
        tag_names = await self._extract_hashtags(self.content)
        for name in tag_names:
            tag = await Tag.get_or_create(name=name.lower())
            tag = tag[0]
            if not tag.creator_id:
                tag.creator_id = self.creator_id
                await tag.save()
                
            await self.tags.add(tag)
            await self.save()
            
    async def _extract_hashtags(self, content: str) -> List[str]:
        regex = "#(\w+)"
        hashtag_list = re.findall(regex, content)
        
        return hashtag_list