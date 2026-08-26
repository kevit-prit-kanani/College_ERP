from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import TypeAdapter

from libs.utils.comman.auth.token_generation import require_roles
from libs.utils.comman.customs.variables import PyObjectId
from libs.utils.comman.models.APIResponse import (
    DBResponse,
    DeleteEffect,
    InsertEffect,
    UpdateEffect,
)
from libs.utils.comman.models.Department import GetAllDepartment
from libs.utils.db.mongodb import db_Department

department_admin = APIRouter(
    tags=["Department"],
    dependencies=[Depends(require_roles("Admin"))],
)


@department_admin.get("/department")
def get_all_departmen(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    department_list = db_Department.find().skip(skip=skip).limit(limit=limit)
    response = TypeAdapter(list[GetAllDepartment]).validate_python(department_list)
    return response


@department_admin.post("/department")
def create_department(name: str):
    result = db_Department.insert_one({"name": name})
    return DBResponse(
        id=result.inserted_id,
        total_records=InsertEffect(created_count=1),
        items=[],
        message="Department Created Successfully",
    )


@department_admin.put("/department/{department_id}")
def update_department(department_id: PyObjectId, name: str):
    result = db_Department.update_one({"_id": department_id}, {"$set": {"name": name}})
    response = DBResponse(
        id=department_id,
        total_records=UpdateEffect(
            match_count=result.matched_count,
            update_count=result.modified_count,
        ),
        items=[],
        message="Department updated successfully",
    )
    return response


@department_admin.delete("/department/{department_id}")
def delete_department(department_id: PyObjectId):
    result = db_Department.delete_one({"_id": department_id})
    response = DBResponse(
        id=department_id,
        total_records=DeleteEffect(deleted_count=result.deleted_count),
        items=[],
        message="Department Deleted successfully",
    )
    return response
