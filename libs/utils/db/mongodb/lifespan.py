from contextlib import asynccontextmanager

from fastapi import FastAPI

from libs.utils.db.mongodb import db_Intakes


@asynccontextmanager
async def lifespan(app: FastAPI):

    db_Intakes.create_index(
        [
            ("year", 1),
            ("department_id", 1),
        ],
        unique=True,
        name="unique_year_department",
    )

    yield
