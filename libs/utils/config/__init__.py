import os
from pathlib import Path

from dotenv import load_dotenv

# Load a local .env file when running the application directly on a developer
# machine. In Docker and production, values are supplied by the environment;
# existing environment variables always take precedence over a local file.
load_dotenv(override=False)


def required_env(name: str) -> str:
    """Return a required setting without ever providing an insecure default."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is not set: {name}")
    return value


AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

HOST = os.getenv("HOST", "localhost")

FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "8000"))

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

FASTAPI_DATABASE_NAME = os.getenv("FASTAPI_DATABASE_NAME", "ERP")

UPLOAD_DIR = Path(os.getenv("FILE_PATH", "uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)


USERS_COLLECTION = os.getenv("USERS_COLLECTION", "users")
SECRET_KEY = required_env("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
