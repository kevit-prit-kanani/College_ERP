from pydantic import BaseModel, Field

from libs.utils.comman.customs.variables import PyObjectId


class CreateIntake(BaseModel):
    department_id: PyObjectId
    totalStudentsIntake: int


class IntakeBranchResponse(BaseModel):
    department_id: PyObjectId
    department_name: str
    totalStudentsIntake: int


class GetAllIntakes(BaseModel):
    id: PyObjectId = Field(alias="_id")
    year: int = Field(gt=1900, lt=2100)
    branches: list[IntakeBranchResponse]


class UpdateIntake(CreateIntake):
    pass
