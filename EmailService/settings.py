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
    "common.events.models",
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


# sendgrid settings
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
MAIN_EMAIL_TEMPLATE = os.getenv('MAIN_EMAIL_TEMPLATE')
FRONTEND_URL = os.getenv('FRONTEND_URL')
NO_REPLY_EMAIL = "no-reply@microsociety.pl"
PASS_RESET_ENDPOINT = 'accounts/passwordReset'


# broker settings
BROKER_URL = os.getenv('BROKER_URL')
QUEUE = 'email_queue'
EXCHANGE = 'email_exchange'

BINDINGS = {
    'account_exchange': 
        ('account.password_reset', 
         'blog_user.created',
         'blog_user.deleted',
         'employee.created'),
}


# auth settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"


# web connection settings
FRONTEND_URL = os.getenv('FRONTEND_URL')
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL
]

CORS_ALLOWED_METHODS = ["*"]
CORS_ALLOWED_HEADERS = ["*"]
ALLOWED_HOSTS = ["*"]