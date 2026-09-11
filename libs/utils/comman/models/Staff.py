from typing import Literal

from libs.utils.comman.models.User import CreateUserRequest, UserResponse


class GetStaffResponse(UserResponse):
    role: Literal["Admin", "Staff"]


class CreateStaffRequest(CreateUserRequest):
    role: Literal["Admin", "Staff"]
    hash_password: str


class UpdateStaffRequest(CreateUserRequest):
    is_active: bool
    is_deleted: bool
