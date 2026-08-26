from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import TypeAdapter

from libs.utils.comman.models.Staff import CreateStaffRequest, GetStaffResponse
from libs.utils.db.mongodb import db_Staff

staff = APIRouter(tags=["Staff"])


@staff.get("/staff")
def get_all_staff(
    skip: Annotated[int, Query()] = 0, limit: Annotated[int, Query()] = 10
):
    """Get all students with pagination."""
    students_list = list(db_Staff.find().skip(skip).limit(limit))
    response = TypeAdapter(list[GetStaffResponse]).validate_python(students_list)
    return response


@staff.post("/staff")
def Create_staff(staff_data: CreateStaffRequest):
    new_staff = staff_data.model_dump(by_alias=False, exclude_unset=False)
    result = db_Staff.insert_one(new_staff)

    new_staff["_id"] = result.inserted_id
    response = GetStaffResponse(**new_staff)
    return response
