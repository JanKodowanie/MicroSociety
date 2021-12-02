import os
import logging
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger('uvicorn')


# broker settings
BROKER_URL = os.getenv('BROKER_URL')
QUEUE = 'email_queue'
EXCHANGE = 'email_exchange'

BINDINGS = {
    'email_exchange': ('email.a', 'email.b'),
    'account_exchange': ('account',)
}


# auth settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30