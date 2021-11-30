import aio_pika as pika
import settings
import json
import uuid
import sys
from settings import logger


class BrokerClient:
    
    def __init__(self, callable):
        self.callable = callable
        self.connection = None
        self.pub_channel = None
        self.loop = None
        
    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        self.loop = loop
        try:
            self.connection = await pika.connect_robust(settings.BROKER_URL,
                                        loop=self.loop)
        except Exception as e:
            logger.error("Error connecting to broker")
            sys.exit(-1)
            
        channel = await self.connection.channel()
        queue = await channel.declare_queue(settings.CONSUMER_QUEUE)
        await queue.consume(self._process_incoming_message, no_ack=False)
        logger.info('Established async broker listener')
        return self.connection
    
    async def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        """Can be used ONLY after consume is run somewhere"""
        
        if not self.pub_channel:
            self.pub_channel = await self.connection.channel()
        
        routing_key = settings.ROUTING_KEY

        await self.pub_channel.default_exchange.publish(
            pika.Message(body=json.dumps(message).encode(), correlation_id=str(uuid.uuid4())),
            routing_key='test'
        )
    
    async def _process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        message.ack()
        body = message.body
        if body:
            self.callable(json.loads(body))