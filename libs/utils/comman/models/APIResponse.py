from pydantic import BaseModel

from libs.utils.comman.customs.variables import PyObjectId


class InsertEffect(BaseModel):
    created_count: int


class UpdateEffect(BaseModel):
    match_count: int
    update_count: int


class DeleteEffect(BaseModel):
    deleted_count: int


class DBResponse(BaseModel):
    id: PyObjectId | None
    total_records: UpdateEffect | DeleteEffect | InsertEffect
    items: list[dict]
    message: str = ""
