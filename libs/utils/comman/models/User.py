from datetime import date, datetime
from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr


class Users(BaseModel):
    model_config = ConfigDict(use_bson=True)

    user_id = ObjectId
    first_name: str
    last_name: str
    email: EmailStr
    hash_password: str
    birthDate: date
    age: int | None
    education: str | None
    created_At: datetime
    modified_At: datetime | None
    department_id: ObjectId | None
    is_Active: bool = True
    is_deleted: bool = False


class Staff(Users):
    role: Literal["admin", "staff"] = "Staff"


class Students(Users):
    enrollment_number : str
    batch: str
    semester: int

class User_wise_Department(BaseModel):
    user_id: ObjectId
    department_idL: ObjectId