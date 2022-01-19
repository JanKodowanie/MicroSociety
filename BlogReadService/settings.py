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
    'blog_write_exchange': ('post.*', 'comment.*', 'like.*'),
    'account_exchange': ('blog_user.*',),
}


# web connectio settings
FRONTEND_URL = os.getenv('FRONTEND_URL')
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL
]

CORS_ALLOWED_METHODS = ["*"]
CORS_ALLOWED_HEADERS = ["*"]
ALLOWED_HOSTS = ["*"]