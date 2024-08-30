import os
from dotenv import load_dotenv
load_dotenv()  

DATABASE_URL = os.getenv('DATABASE_URL')
valid_extensions = os.getenv('EXTENSIONS')