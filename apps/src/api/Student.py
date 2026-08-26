from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Header, Query
from pydantic import TypeAdapter

from libs.utils.comman.auth.token_generation import require_roles
from libs.utils.comman.customs.variables import PyObjectId
from libs.utils.comman.models.APIResponse import DBResponse, DeleteEffect, UpdateEffect
from libs.utils.comman.models.Student import (
    CreateStudentRequest,
    GetStudentResponse,
    UpdateStudentRequest,
)
from libs.utils.db.mongodb import db_Student

student_admin_staff = APIRouter(
    tags=["Student"],
    dependencies=[Depends(require_roles("Admin", "Staff"))],
)

student_all_roles = APIRouter(
    tags=["Student"],
    dependencies=[Depends(require_roles("Admin", "Staff", "Student"))],
)


@student_admin_staff.get("/student")
async def get_all_students(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    """Get all students with pagination."""
    students_list = list(db_Student.find().skip(skip).limit(limit))
    response = TypeAdapter(list[GetStudentResponse]).validate_python(students_list)
    return response


@student_admin_staff.post("/student")
async def create_student(student_data: CreateStudentRequest):
    # Convert Pydantic model to dict - PyObjectId stays as ObjectId
    new_student = student_data.model_dump(by_alias=False, exclude_unset=False)
    new_student.update({
                "is_active": True,
                "is_deleted": False,
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            })
    result = db_Student.insert_one(new_student)

    new_student["_id"] = result.inserted_id
    response = GetStudentResponse(**new_student)
    return response


@student_all_roles.get("/student/{student_id}")
async def get_student_by_id(student_id: PyObjectId):
    student = db_Student.find_one({"_id": student_id})
    response = GetStudentResponse(**student)
    return response


@student_all_roles.put("/student/{student_id}")
async def update_student(
    student_id: PyObjectId, student: Annotated[UpdateStudentRequest, Body()]
):
    update_data = student.model_dump(exclude_unset=True)
    result = db_Student.update_one({"_id": student_id}, {"$set": update_data})
    response = DBResponse(
        id=student_id,
        total_records=UpdateEffect(
            match_count=result.matched_count,
            update_count=result.modified_count,
        ),
        items=[],
        message="Student updated successfully",
    )
    return response


@student_admin_staff.delete("/student")
async def delete_student(student_id: Annotated[PyObjectId, Header()]):
    result = db_Student.delete_one({"_id": student_id})
    response = DBResponse(
        id=student_id,
        total_records=DeleteEffect(deleted_count=result.deleted_count),
        items=[],
        message="Student Deleted successfully",
    )
    return response
