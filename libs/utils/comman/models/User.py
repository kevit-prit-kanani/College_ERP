from pydantic import BaseModel, ConfigDict, EmailStr, Field

from libs.utils.comman.customs.variables import PyObjectId


class UserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    age: int | None
    education: str | None
    department_id: PyObjectId
    is_Active: bool = True
    is_deleted: bool = False


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str
    email: EmailStr
    age: int | None = None
    education: str | None = None
    department_id: PyObjectId
