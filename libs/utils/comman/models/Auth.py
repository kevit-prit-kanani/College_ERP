from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from libs.utils.comman.models.Staff import CreateStaffRequest
from libs.utils.comman.models.Student import CreateStudentRequest


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)
    role: Literal["Staff", "Student"]


class StaffRegisterRequest(CreateStaffRequest):
    password: str


class StudentRegisterRequest(CreateStudentRequest):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
