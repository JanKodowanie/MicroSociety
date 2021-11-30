from fastapi import FastAPI
from common.broker.client import BrokerClient
from settings import logger


class ESApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broker_client = BrokerClient()

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        logger.info('Received message:')
        logger.info(message)