from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from apps.src.main import api
from libs.utils.config import MONGODB_URL
from libs.utils.logging_config import setup_logging

setup_logging()

app = FastAPI()


app.include_router(api)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=307)


client = MongoClient(MONGODB_URL)

db = client["ERP"]


@app.get("/ping")
async def mongodb_health_check():
    try:
        db.client.admin.command("ping")

        return {
            "status": "healthy",
            "mongodb": "connected",
        }

    except PyMongoError as e:
        return {
            "status": "unhealthy",
            "mongodb": "disconnected",
            "error": str(e),
        }
