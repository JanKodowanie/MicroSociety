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
            
            if settings.EXCHANGE:
                self.pub_channel = await self.connection.channel()
                self.exchange = await self.pub_channel.declare_exchange(settings.EXCHANGE, 
                                        pika.ExchangeType.TOPIC, durable=True)
                
            if settings.QUEUE:
                self.sub_channel = await self.connection.channel()
                self.queue = await self.sub_channel.declare_queue(settings.QUEUE, durable=True)
                
                if settings.BINDINGS:
                    for exchange, binding_keys in settings.BINDINGS.items():
                        await self.sub_channel.declare_exchange(exchange, 
                                        pika.ExchangeType.TOPIC, durable=True)
                        for key in binding_keys:
                            await self.queue.bind(exchange, key)
                            
        except Exception as e:
            logger.error("Error connecting to the broker.")
            logger.error(e)
            sys.exit(-1) 
    
    async def consume(self):    
        await self.queue.consume(self._process_incoming_message, no_ack=False)
        logger.info('Established async broker listener.')
        return self.connection
    
    async def send_message(self, message: dict, routing_key: str):
        """Method to publish message to RabbitMQ"""
        message['event'] = routing_key
        await self.exchange.publish(
            message=pika.Message(body=json.dumps(message).encode(), message_id=str(uuid.uuid4())),
            routing_key=routing_key
        )
        logger.info('Published event: ' + str(message))
    
    async def _process_incoming_message(self, message: pika.Message):
        """Processing incoming message from RabbitMQ"""
        message.ack()
        body = message.body
        if body:
            logger.info('Received event: ' + str(body.decode()))
            await self.callable(json.loads(body))
        