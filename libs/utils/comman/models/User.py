from pydantic import ConfigDict, EmailStr

from libs.utils.comman.customs.variables import MongoBaseModel, PyObjectId


class UserResponse(MongoBaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId
    first_name: str
    last_name: str
    email: EmailStr
    age: int | None
    education: str | None
    department_name: str | None = None
    is_active: bool = True
    is_deleted: bool = False


class CreateUserRequest(MongoBaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str
    email: EmailStr
    age: int | None = None
    education: str | None = None
    department_id: PyObjectId
