from os import path
from pathlib import Path

from dotenv import dotenv_values

env_path = ".env"

if not path.exists(env_path):
    raise FileNotFoundError(f".env file not found at {env_path}")

config = dotenv_values(env_path)

AUTH_USERNAME = config.get("AUTH_USERNAME")
AUTH_PASSWORD = config.get("AUTH_PASSWORD")

HOST = config.get("HOST")

FASTAPI_PORT = int(config.get("FASTAPI_PORT"))

MONGODB_URL = config.get("MONGODB_URL", "localhost")

FASTAPI_DATABASE_NAME = config.get("FASTAPI_DATABASE_NAME")

UPLOAD_DIR = Path(config.get("FILE_PATH"))
UPLOAD_DIR.mkdir(exist_ok=True)


USERS_COLLECTION = config.get("USERS_COLLECTION")
SECRET_KEY = config.get("SECRET_KEY", "This_is_the_secrate_key_")
ALGORITHM = config.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
