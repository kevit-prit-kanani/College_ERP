import logging
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import TypeAdapter
from pymongo.errors import DuplicateKeyError

from libs.utils.comman.auth.token_generation import require_roles
from libs.utils.comman.customs.variables import PyObjectId
from libs.utils.comman.models.APIResponse import (
    DBResponse,
    InsertEffect,
    UpdateEffect,
)
from libs.utils.comman.models.Intakes import CreateIntake, GetAllIntakes, UpdateIntake
from libs.utils.db.mongodb import db_Intakes

looger = logging.getLogger(__name__)
intakes_admin = APIRouter(
    tags=["Intakes"],
    dependencies=[Depends(require_roles("Admin"))],
)


@intakes_admin.get("/intakes")
def get_all_intakes():

    pipeline = [
        {"$unwind": "$branches"},
        {
            "$lookup": {
                "from": "Department",
                "localField": "branches.department_id",
                "foreignField": "_id",
                "as": "department",
            }
        },
        {"$unwind": "$department"},
        {
            "$group": {
                "_id": "$_id",
                "year": {"$first": "$year"},
                "branches": {
                    "$push": {
                        "department_id": "$branches.department_id",
                        "department_name": "$department.name",
                        "totalStudentsIntake": "$branches.totalStudentsIntake",
                    }
                },
            }
        },
    ]

    intakes_list = list(db_Intakes.aggregate(pipeline))

    response = TypeAdapter(list[GetAllIntakes]).validate_python(intakes_list)

    return response


@intakes_admin.post("/intakes")
def create_current_year_intakes(create_intakes: CreateIntake):

    current_year = datetime.now(tz=UTC).year

    branch = {
        "department_id": create_intakes.department_id,
        "totalStudentsIntake": create_intakes.totalStudentsIntake,
    }

    document = {
        "year": current_year,
        "branches": [branch],
    }

    try:
        result = db_Intakes.insert_one(document)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail=f"Intakes for year {current_year} already exist.",
        )

    document["_id"] = result.inserted_id

    return document


@intakes_admin.put("/intakes")
def update_current_year_intakes(create_intakes: CreateIntake):

    current_year = datetime.now(tz=UTC).year

    branch = {
        "department_id": create_intakes.department_id,
        "totalStudentsIntake": create_intakes.totalStudentsIntake,
    }

    result = db_Intakes.update_one(
        {
            "year": current_year,
            "branches": {
                "$not": {"$elemMatch": {"department_id": create_intakes.department_id}}
            },
        },
        {"$push": {"branches": branch}},
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Department {create_intakes.department_id} "
                f"already exists for year {current_year}"
            ),
        )

    return DBResponse(
        id=None,
        total_records=UpdateEffect(
            match_count=result.matched_count,
            update_count=result.modified_count,
        ),
        items=[],
        message="Current Year Intake Is Updated!",
    )


@intakes_admin.patch("/intakes")
def update_department_intake(create_intakes: CreateIntake):

    current_year = datetime.now(tz=UTC).year

    result = db_Intakes.update_one(
        {
            "year": current_year,
            "branches.department_id": create_intakes.department_id,
        },
        {
            "$set": {
                "branches.$.totalStudentsIntake": create_intakes.totalStudentsIntake
            }
        },
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Department {create_intakes.department_id} "
                f"does not have an intake for {current_year}."
            ),
        )

    return DBResponse(
        id=None,
        total_records=UpdateEffect(
            match_count=result.matched_count,
            update_count=result.modified_count,
        ),
        items=[],
        message="Current Year's Department Intake Is Updated!",
    )
