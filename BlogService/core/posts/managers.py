from .models import *
from .schemas import *


class BlogPostManager:
    
    async def create_blog_post(self, post_content: BlogPostCreateSchema):
        instance = await BlogPost.create(**post_content.dict())
        await instance.create_tags_from_content()
        await instance.fetch_related('tags')
        return instance
    
    async def get_posts(self):
        posts = await BlogPost.all().prefetch_related('tags')
        return posts
        