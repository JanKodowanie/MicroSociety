from fastapi import Request
from .published import *
from common.events.models import *
from core.models import Post, Comment
from common.events.broker_client import BrokerClient
from common.enums import *


class EventPublisher:
    
    def __init__(self, request: Request):
        self.broker: BrokerClient = request.app.broker_client
        
    async def _publish_event(self, body: str, routing_key: str, message_id: str):
        await self.broker.send_message(body, routing_key, 'blog_write', message_id)
        
    async def publish_post_created(self, instance: Post):
        message_schema = PostCreated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_post_updated(self, instance: Post):
        message_schema = PostUpdated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_post_deleted(self, post_id: int):
        message_schema = PostDeleted(id=post_id)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_comment_created(self, instance: Comment):
        message_schema = CommentCreated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_comment_updated(self, instance: Comment):
        message_schema = CommentUpdated.from_orm(instance)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_comment_deleted(self, post_id: int, comment_id: int):
        message_schema = CommentDeleted(post_id=post_id, id=comment_id)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_like_created(self, creator_id: UUID, post_creator_id: UUID, post_id: int):
        message_schema = LikeCreated(creator_id=creator_id, post_creator_id=post_creator_id, post_id=post_id)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_like_deleted(self, creator_id: UUID, post_creator_id: UUID, post_id: int):
        message_schema = LikeDeleted(creator_id=creator_id, post_creator_id=post_creator_id, post_id=post_id)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event)
        
        await self._publish_event(body, event.name, event.id)