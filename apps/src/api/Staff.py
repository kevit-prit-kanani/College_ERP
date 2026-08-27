from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import TypeAdapter

from libs.utils.comman.auth.token_generation import require_roles
from libs.utils.comman.customs.HashPass import get_hashed_password
from libs.utils.comman.customs.variables import PyObjectId
from libs.utils.comman.exceptions import AuthorizationError
from libs.utils.comman.models.APIResponse import DBResponse, DeleteEffect, UpdateEffect
from libs.utils.comman.models.Staff import (
    CreateStaffRequest,
    GetStaffResponse,
    UpdateStaffRequest,
)
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


@staff.get("/staff/{staff_id}")
def get_staff_by_id(staff_id: PyObjectId):
    staff_by_id = db_Staff.find_one({"_id": staff_id})
    response = GetStaffResponse(**staff_by_id)
    return response


@staff_admin.post("/staff")
def create_staff(staff_data: CreateStaffRequest):
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


@staff_admin.put("/staff")
def update_staff(staff_data: UpdateStaffRequest):
    new_staff = staff_data.model_dump(by_alias=False, exclude_unset=False)
    staff_id = new_staff.pop("id")
    new_staff.update(
        {
            "updated_at": datetime.now(UTC),
        }
    )
    result = db_Staff.update_one({"_id": staff_id}, {"$set": new_staff})
    response = DBResponse(
        id=staff_id,
        total_records=UpdateEffect(
            match_count=result.matched_count,
            update_count=result.modified_count,
        ),
        items=[],
        message="Staff updated successfully",
    )
    return response


@staff_admin.delete("/staff/{staff_id}")
def delete_staff(staff_id: PyObjectId):
    existing_staff = db_Staff.find_one({"_id": staff_id})
    if existing_staff and existing_staff["role"] == "Admin":
        raise AuthorizationError()

    result = db_Staff.delete_one({"_id": staff_id})
    response = DBResponse(
        id=staff_id,
        total_records=DeleteEffect(deleted_count=result.deleted_count),
        items=[],
        message="Student Deleted successfully",
    )
    return response
