import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

VALID_EXTENSIONS = os.getenv('EXTENSIONS').split(',')

ALLOW_ORIGINS = os.getenv('ALLOW_ORIGINS').split(',')
ALLOW_CREDENTIALS = os.getenv('ALLOW_CREDENTIALS').lower() == 'true'
ALLOW_METHODS = os.getenv('ALLOW_METHODS').split(',')
ALLOW_HEADERS = os.getenv('ALLOW_HEADERS').split(',')
