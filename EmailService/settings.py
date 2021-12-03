import os
import logging
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger('uvicorn')


# sendgrid settings
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
MAIN_EMAIL_TEMPLATE = os.getenv('MAIN_EMAIL_TEMPLATE')
DOMAIN = "https://microsociety.pl"
NO_REPLY_EMAIL = "no-reply@microsociety.pl"
PASS_RESET_ENDPOINT = 'accounts/passwordReset'


# broker settings
BROKER_URL = os.getenv('BROKER_URL')
QUEUE = 'email_queue'
EXCHANGE = 'email_exchange'

BINDINGS = {
    'account_exchange': ('account.password_reset', 'account.created')
}


# auth settings
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30