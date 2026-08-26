from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import TypeAdapter

from libs.utils.comman.auth.token_generation import require_roles
from libs.utils.comman.customs.variables import PyObjectId
from libs.utils.comman.models.APIResponse import (
    DBResponse,
    InsertEffect,
    UpdateEffect,
)
from libs.utils.comman.models.Intakes import CreateIntake, GetAllIntakes, UpdateIntake
from libs.utils.db.mongodb import db_Intakes

intakes_admin = APIRouter(
    tags=["Intakes"],
    dependencies=[Depends(require_roles("Admin"))],
)


@intakes_admin.get("/intakes")
def get_all_intakes(
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    intakes_list = db_Intakes.find().skip(skip).limit(limit)
    response = TypeAdapter(list[GetAllIntakes]).validate_python(intakes_list)
    return response


@intakes_admin.post("/intakes")
def create_current_year_intakes(create_intakes: CreateIntake):
    new_intake = create_intakes.model_dump()
    new_intake.update({"year": datetime.now(tz=UTC).year})
    result = db_Intakes.insert_one(new_intake)
    response = DBResponse(
        id=result.inserted_id,
        total_records=InsertEffect(created_count=1),
        items=[],
        message="Current Year Intake Is Updated!",
    )
    return response


@intakes_admin.put("/intakes/{intake_id}")
def Update_current_year_intakes(intake_id: PyObjectId, update_intakes: UpdateIntake):
    update_intakes = update_intakes.model_dump()
    result = db_Intakes.update_one(update_intakes)
    response = DBResponse(
        id=result.inserted_id,
        total_records=UpdateEffect(
            match_count=result.matched_count, update_count=result.modified_count
        ),
        items=[],
        message="Current Year Intake Is Updated!",
    )
    return response
