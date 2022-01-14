from fastapi import FastAPI
from common.broker.client import BrokerClient


class MSApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broker_client = BrokerClient()