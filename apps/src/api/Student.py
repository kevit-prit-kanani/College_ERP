from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import TypeAdapter

from libs.utils.comman.models.Student import CreateStudentRequest, GetStudentResponse
from libs.utils.db.mongodb import db_Students

student = APIRouter()


@student.get("/student")
async def get_all_students(
    skip: Annotated[int, Query()] = 0, limit: Annotated[int, Query()] = 10
):
    """Get all students with pagination."""
    students_list = list(db_Students.find().skip(skip).limit(limit))
    response = TypeAdapter(list[GetStudentResponse]).validate_python(students_list)
    return response


@student.post("/student")
async def create_student(student_data: CreateStudentRequest):
    """Create a new student."""
    # Convert Pydantic model to dict - PyObjectId stays as ObjectId
    new_student = student_data.model_dump(by_alias=False, exclude_unset=False)

    # Insert into MongoDB
    result = db_Students.insert_one(new_student)

    # Add the inserted ID to the response
    new_student["_id"] = result.inserted_id

    # Return as GetStudentResponse - PyObjectId will convert _id to str automatically
    return GetStudentResponse(**new_student)
