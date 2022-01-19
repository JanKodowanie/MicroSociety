import os
import logging
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise


load_dotenv()
logger = logging.getLogger('uvicorn')


# db settings

DATABASE_URL = os.getenv('DATABASE_URL')

MODEL_PATHS = (
    "core.models",
    "common.events.models",
    "common.auth.models",
    "aerich.models"
)

DB_CONFIG = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": MODEL_PATHS,
            "default_connection": "default"
        },
    },
}

def create_db_connection(app) -> None:
    register_tortoise(
        app,
        DB_CONFIG
    )

Tortoise.init_models(MODEL_PATHS, 'models')


# broker settings
BROKER_URL = os.getenv('BROKER_URL')
QUEUE = 'blog_write_queue'
EXCHANGE = 'blog_write_exchange'

BINDINGS = {
    'account_exchange': ('blog_user.deleted', 'account.full_logout'),
}


# auth settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"


# media settings
MEDIA_DIR = os.getenv('MEDIA_DIR')
MEDIA_ROOT = '/media'


# web connection settings
FRONTEND_URL = os.getenv('FRONTEND_URL')
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL
]

CORS_ALLOWED_METHODS = ["*"]
CORS_ALLOWED_HEADERS = ["*"]
ALLOWED_HOSTS = ["*"]