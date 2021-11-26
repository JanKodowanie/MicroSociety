from .models import *
from .schemas import *
from .exceptions import *
from tortoise.exceptions import DoesNotExist


class BlogPostManager:
    
    async def create_blog_post(self, post_content: BlogPostCreateSchema) -> BlogPost:
        instance = await BlogPost.create(**post_content.dict())
        await instance.create_tags_from_content()
        await instance.fetch_related('tags')
        return instance
    
    async def get_post_by_id(self, post_id: int) -> BlogPost:
        try:
            instance = await BlogPost.get(post_id=post_id)
        except DoesNotExist:
            raise BlogNotFound()
        
        return instance
    
    async def delete_blog_post(self, post: BlogPost) -> None:
        await post.delete()

    async def get_posts(self, filters: dict = None) -> List[BlogPost]:
        if not filters:
            posts = await BlogPost.all().prefetch_related('tags')
        else:
            posts = await BlogPost.filter(**filters).prefetch_related('tags')
        return posts
    

class TagManager:
    
    async def get_tag_list(self) -> List[Tag]:
        return await Tag.all()
    
    async def get_posts_in_tag(self, tag_name: str) -> List[BlogPost]:
        try:
            tag = await Tag.get(name=tag_name)
        except DoesNotExist:
            raise TagNotFound()
        await tag.fetch_related('posts')
        return await tag.posts.all().prefetch_related('tags')
        