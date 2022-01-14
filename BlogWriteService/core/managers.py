from .models import *
from .schemas import *
from .exceptions import *
from fastapi import Depends, UploadFile
from tortoise.exceptions import DoesNotExist
from common.file_manager import FileManager
from core.events.event_publisher import EventPublisher


class TagManager:
    
    async def create_tags_from_post(self, post: Post):
        tag_names = await post.extract_hashtags()
        for name in tag_names:
            tag = await Tag.get_or_create(name=name.lower())
            tag = tag[0]
            tag.popularity += 1
            await tag.save()
                
            await post.tags.add(tag)
            await post.save()
    
    async def decrease_post_tags_popularity(self, post: Post):
        for tag in post.tags:
            tag.popularity -= 1
            if tag.popularity != 0:
                await tag.save()
            else:
                await tag.delete()
    
    async def get_tag_list(self) -> List[Tag]:
        return await Tag.all().order_by('-popularity')
    
    async def get_posts_in_tag(self, tag_name: str) -> List[Post]:
        try:
            tag = await Tag.get(name=tag_name)
        except DoesNotExist:
            raise TagNotFound()
        await tag.fetch_related('posts')
        return await tag.posts.all().prefetch_related('tags')


class PostManager:
    
    def __init__(self, tag_manager: TagManager = Depends(), broker: EventPublisher = Depends()):
        self.tag_manager = tag_manager
        self.broker = broker

    async def create(self, creator_id: UUID, 
                               content: str, picture: Optional[UploadFile]) -> Post:
        
        data = PostCreateSchema(content=content).dict()
        if picture:
            try:
                FileManager().validate_file(picture, ['jpg', 'jpeg', 'png'])
            except Exception as e:
                error = {'picture': e.detail}
                raise InvalidBlogPostData('Uploaded file is not a valid picture', detail=error)   
                
        instance = await Post.create(creator_id=creator_id, **data)
        if picture:
            path, url = FileManager().upload_file(picture, instance.id, 'post_pics', ['jpg', 'jpeg', 'png'])
            instance.picture_path = path
            instance.picture_url = url
            await instance.save()
        
        await self.tag_manager.create_tags_from_post(instance)
        await instance.fetch_related('tags', 'comments')
        await self.broker.publish_post_created(instance)
        return instance
    
    async def get(self, id: int) -> Post:
        try:
            instance = await Post.get(id=id)
        except DoesNotExist:
            raise PostNotFound()
        
        await instance.fetch_related('tags', 'comments')
        return instance

    async def edit(self, instance: Post, 
                        new_content: Optional[str], delete_picture: bool, new_picture: Optional[UploadFile]) -> Post:
        if new_picture:
            try:
                path, url = FileManager().upload_file(new_picture, instance.id, 'post_pics', ['jpg', 'jpeg', 'png'])
                instance.picture_path = path
                instance.picture_url = url
                await instance.save()
            except Exception as e:
                error = {'picture': e.detail}
                raise InvalidBlogPostData('Uploaded file is not a valid picture', detail=error)
        elif delete_picture:
            await self.delete_picture(instance)
            
        if new_content:
            await self.tag_manager.decrease_post_tags_popularity(instance)
            await instance.tags.clear()
            instance.content = PostCreateSchema(content=new_content).content
            await instance.save()
            await self.tag_manager.create_tags_from_post(instance)
        
        await instance.fetch_related('tags', 'comments')
        await self.broker.publish_post_updated(instance)
        return instance
    
    async def delete(self, instance: Post):
        await self.tag_manager.decrease_post_tags_popularity(instance)
        id = instance.id
        await instance.delete()
        await self.broker.publish_post_deleted(id)

    async def get_list(self, filters: dict = None) -> List[Post]:
        if not filters:
            posts = await Post.all().prefetch_related('tags')
        else:
            posts = await Post.filter(**filters).prefetch_related('tags')
        return posts
    
    async def bulk_delete(self, filters: dict = None):
        posts = await Post.filter(**filters).prefetch_related('tags')
        for post in posts:
            await TagManager().decrease_post_tags_popularity(post)
            await post.delete()
            
    async def delete_picture(self, instance: Post):
        if instance.picture_path:
            FileManager().delete_file(instance.picture_path)
        instance.picture_path = None
        instance.picture_url = None
        await instance.save()