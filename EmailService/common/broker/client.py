import aio_pika as pika
import settings
import json
import uuid
import sys
from settings import logger


class BrokerClient:
    
    async def initialize(self, loop, callable):
        self.callable = callable
        self.loop = loop
        try:
            self.connection = await pika.connect_robust(settings.BROKER_URL,
                                        loop=self.loop)
            self.sub_channel = await self.connection.channel()
            self.pub_channel = await self.connection.channel()
            self.queue = await self.sub_channel.declare_queue('account_sub', durable=True)
            self.exchange = await self.sub_channel.declare_exchange('account_pub', 
                                    pika.ExchangeType.TOPIC, durable=True)
            
            await self.queue.bind('account_pub', 'account.test')
        except Exception as e:
            logger.error("Error connecting to broker")
            logger.error(e)
            sys.exit(-1) 
    
    async def consume(self):    
        await self.queue.consume(self._process_incoming_message, no_ack=False)
        logger.info('Established async broker listener')
        return self.connection
    
    async def send_message(self, message: dict, routing_key: str):
        """Method to publish message to RabbitMQ"""
        
        await self.pub_channel.basic_publish(
            exchange='account',
            body=pika.Message(body=json.dumps(message).encode(), correlation_id=str(uuid.uuid4())),
            routing_key=routing_key
        )
    
    async def _process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        message.ack()
        body = message.body
        if body:
            self.callable(json.loads(body))