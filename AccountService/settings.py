import os
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise


load_dotenv()

# db settings

DATABASE_URL = os.getenv('DATABASE_URL')

MODEL_PATHS = (
    "core.accounts.models",
)


def create_db_connection(app) -> None:
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={'models': MODEL_PATHS},
        generate_schemas=True,
        add_exception_handlers=True
    )


# auth settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30