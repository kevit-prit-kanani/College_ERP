from pymongo import MongoClient
from pymongo.errors import PyMongoError

from libs.utils.config import (
    FASTAPI_DATABASE_NAME,
    MONGODB_URL,
)


def connect_db(db_name: str):
    try:
        client = MongoClient(MONGODB_URL)
        return client[db_name]
    except PyMongoError as error:
        raise Exception(  # noqa: TRY002
            f'Failed to connect to database: "{db_name}",' f"ERROR: {error!s}"
        )


db = connect_db(FASTAPI_DATABASE_NAME)

db_Students = db["Students"]
db_Staff = db["Staff"]
db_Attendance = db["Attendance"]
db_Batches = db["Batches"]
db_Department = db["Department"]
db_User_wise_Department = db["User_wise_Department"]
