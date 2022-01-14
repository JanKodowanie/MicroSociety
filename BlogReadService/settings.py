import os
import logging
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger('uvicorn')


# db settings

DATABASE_URL = os.getenv('DATABASE_URL')

# broker settings
BROKER_URL = os.getenv('BROKER_URL')
QUEUE = 'blog_read_queue'
EXCHANGE = 'blog_read_exchange'

BINDINGS = {
    'blog_write_exchange': ('post.*', 'comment.*'),
    'account_exchange': ('blog_user.*',),
}