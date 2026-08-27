# role: Literal["Admin", "Staff", "Student"]

from typing import Literal

from pydantic import Field

from libs.utils.comman.customs.variables import PyObjectId
from libs.utils.comman.models.User import CreateUserRequest, UserResponse


class GetStaffResponse(UserResponse):
    role: Literal["Admin", "Staff"]


class CreateStaffRequest(CreateUserRequest):
    role: Literal["Admin", "Staff"]
    hash_password: str

class UpdateStaffRequest(CreateUserRequest):
    id: PyObjectId = Field(alias='_id')
    is_active: bool
    is_deleted: bool