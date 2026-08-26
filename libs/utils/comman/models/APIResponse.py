from pydantic import BaseModel

from libs.utils.comman.customs.variables import PyObjectId


class UpdateEffect(BaseModel):
    match_count: int
    update_count: int


class DeleteEffect(BaseModel):
    deleted_count: int


class DBResponse(BaseModel):
    id: PyObjectId | None
    total_records: UpdateEffect | DeleteEffect
    items: list[dict]
    message: str = ""
