from starlette.config import Config
from starlette.datastructures import Secret

# Linking .env file 
try:
    config = Config(".env")

except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
  
