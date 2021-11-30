import os
from dotenv import load_dotenv
import logging


load_dotenv()

# broker settings
BROKER_URL = os.getenv('BROKER_URL')
CONSUMER_QUEUE = os.getenv('CONSUMER_QUEUE')
ROUTING_KEY = os.getenv('ROUTING_KEY')

# auth settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


logger = logging.getLogger('uvicorn')