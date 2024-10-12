import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


FLASK_DEBUG = os.getenv('FLASK_DEBUG')
STRING_CHARACTERS = ('abcdefghijklmnopqrstuvwxyz'
                     'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                     '1234567890')
LENGTH_SHORT = 6
MAX_LENGTH_LINK = 16
MAX_LENGTH_ORIGINAL_LINK = 2048
