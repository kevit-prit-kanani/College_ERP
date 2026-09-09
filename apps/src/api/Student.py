import logging
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Header, Query
from pydantic import TypeAdapter

from libs.utils.comman.auth.token_generation import require_roles
from libs.utils.comman.customs.HashPass import get_hashed_password
from libs.utils.comman.customs.variables import PyObjectId
from libs.utils.comman.exceptions import NotFoundError
from libs.utils.comman.models.APIResponse import DBResponse, DeleteEffect, UpdateEffect
from libs.utils.comman.models.Student import (
    CreateStudentRequest,
    GetStudentResponse,
    UpdateStudentRequest,
)
from libs.utils.db.mongodb import db_Student

logger = logging.getLogger(__name__)

student_admin_staff = APIRouter(
    tags=["Student"],
    dependencies=[Depends(require_roles("Admin", "Staff"))],
)

student_all_roles = APIRouter(
    tags=["Student"],
    dependencies=[Depends(require_roles("Admin", "Staff", "Student"))],
)


@student_admin_staff.get("/students")
async def get_all_students(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    pipeline = [
        {
            "$lookup": {
                "from": "Department",
                "localField": "department_id",
                "foreignField": "_id",
                "as": "department",
            },
        },
        {"$unwind": {"path": "$department", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 1,
                "first_name": 1,
                "last_name": 1,
                "email": 1,
                "age": 1,
                "education": 1,
                "department_name": "$department.name",
                "is_active": 1,
                "is_deleted": 1,
                "enrollment_number": 1,
                "batch": 1,
                "semester": 1,
                "admission_year": 1,
            }
        },
        {"$skip": skip},
        {"$limit": limit},
    ]
    students_list = list(db_Student.aggregate(pipeline=pipeline))
    response = TypeAdapter(list[GetStudentResponse]).validate_python(students_list)
    return response


@student_admin_staff.post("/student")
async def create_student(student_data: CreateStudentRequest):

    new_student = student_data.model_dump(exclude_unset=False)
    new_student["hash_password"] = get_hashed_password(student_data.hash_password)
    new_student.update(
        {
            "is_active": True,
            "is_deleted": False,
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        }
    )
    result = db_Student.insert_one(new_student)

    pipeline = [
        {"$match": {"_id": result.inserted_id}},
        {
            "$lookup": {
                "from": "Department",
                "localField": "department_id",
                "foreignField": "_id",
                "as": "department",
            },
        },
        {"$unwind": {"path": "$department", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 1,
                "first_name": 1,
                "last_name": 1,
                "email": 1,
                "age": 1,
                "education": 1,
                "department_name": "$department.name",
                "is_active": 1,
                "is_deleted": 1,
                "enrollment_number": 1,
                "batch": 1,
                "semester": 1,
                "admission_year": 1,
            }
        },
    ]
    inserted_student = next(db_Student.aggregate(pipeline), None)
    response = GetStudentResponse.model_validate(inserted_student)
    return response


@student_all_roles.get("/student/{student_id}")
async def get_student_by_id(student_id: PyObjectId):
    pipeline = [
        {"$match": {"_id": student_id}},
        {
            "$lookup": {
                "from": "Department",
                "localField": "department_id",
                "foreignField": "_id",
                "as": "department",
            },
        },
        {"$unwind": {"path": "$department", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 1,
                "first_name": 1,
                "last_name": 1,
                "email": 1,
                "age": 1,
                "education": 1,
                "department_name": "$department.name",
                "is_active": 1,
                "is_deleted": 1,
                "enrollment_number": 1,
                "batch": 1,
                "semester": 1,
                "admission_year": 1,
            }
        },
    ]
    student = next(db_Student.aggregate(pipeline), None)
    if student is None:
        raise NotFoundError("Student", student_id)

    logger.info("this is the student details: %s", student)
    response = GetStudentResponse.model_validate(student)
    return response.model_dump(mode="json")


@student_all_roles.put("/student/{student_id}")
async def update_student(
    student_id: PyObjectId, student: Annotated[UpdateStudentRequest, Body()]
):
    update_data = student.model_dump(exclude_unset=True)
    update_data.update({"updated_at": datetime.now(UTC)})
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
