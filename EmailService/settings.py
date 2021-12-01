import os
from dotenv import load_dotenv
import logging


load_dotenv()

# broker settings
BROKER_URL = os.getenv('BROKER_URL')
QUEUE = 'email_queue'
EXCHANGE = 'email_exchange'
ROUTING_KEY = os.getenv('ROUTING_KEY')

BINDINGS = {
    'email_exchange': ('email.a', 'email.b'),
    'account_exchange': ('account',)
}


# auth settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


logger = logging.getLogger('uvicorn')