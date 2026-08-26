from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import TypeAdapter

from libs.utils.comman.auth.token_generation import require_roles
from libs.utils.comman.customs.HashPass import get_hashed_password
from libs.utils.comman.models.Staff import CreateStaffRequest, GetStaffResponse
from libs.utils.db.mongodb import db_Staff

staff = APIRouter(
    tags=["Staff"],
    dependencies=[Depends(require_roles("Admin", "Staff"))],
)

staff_admin = APIRouter(
    tags=["Staff"],
    dependencies=[Depends(require_roles("Admin"))],
)


@staff_admin.get("/staff")
def get_all_staff(
    skip: Annotated[int, Query()] = 0, limit: Annotated[int, Query()] = 10
):
    """Get all students with pagination."""
    students_list = list(db_Staff.find().skip(skip).limit(limit))
    response = TypeAdapter(list[GetStaffResponse]).validate_python(students_list)
    return response


@staff_admin.post("/staff")
def Create_staff(staff_data: CreateStaffRequest):
    new_staff = staff_data.model_dump(by_alias=False, exclude_unset=False)
    new_staff["hash_password"] = get_hashed_password(staff_data.hash_password)
    new_staff.update(
        {
            "is_active": True,
            "is_deleted": False,
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        }
    )
    result = db_Staff.insert_one(new_staff)

    new_staff.pop("hash_password")
    new_staff["_id"] = result.inserted_id
    response = GetStaffResponse(**new_staff)
    return response
