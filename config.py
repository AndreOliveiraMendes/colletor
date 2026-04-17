import os

from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv('BASE')
SERVER = os.getenv('SERVER')
LOG = os.getenv('LOG')