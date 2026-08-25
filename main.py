from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from apps.src.main import api

app = FastAPI()


app.include_router(api)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=307)
