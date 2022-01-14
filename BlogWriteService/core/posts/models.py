from tortoise import fields, models
from typing import List
from core.comments.models import Comment
from tortoise.signals import post_delete
from common.file_manager import FileManager
import re


class Tag(models.Model):
    name = fields.CharField(max_length=30, pk=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    popularity = fields.IntField(default=0)
    posts: fields.ManyToManyRelation["BlogPost"]
    
    
class BlogPost(models.Model):
    creator_id = fields.UUIDField()
    content = fields.TextField(max_length=500)
    picture_url = fields.CharField(max_length=300, null=True)
    picture_path = fields.CharField(max_length=300, null=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    tags: fields.ManyToManyRelation["Tag"] \
        = fields.ManyToManyField(model_name='models.Tag', related_name='posts',
                    null=True)
    comments: fields.ManyToManyRelation["Comment"] 
        
    class Meta:
        ordering = ["-date_created"]
            
    async def extract_hashtags(self) -> List[str]:
        regex = "#(\w+)"
        hashtag_list = re.findall(regex, self.content)
        
        return hashtag_list
    
    
@post_delete(BlogPost)
async def blog_post_post_delete(sender, instance, using_db) -> None:
    if instance.picture_path:
        FileManager().delete_file(instance.picture_path)