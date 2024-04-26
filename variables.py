import os

from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')
TOKEN = os.getenv('TOKEN')
