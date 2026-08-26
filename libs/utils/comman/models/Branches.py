from pydantic import BaseModel, Field

from libs.utils.comman.customs.variables import PyObjectId


class Students_Intake(BaseModel):
    name: str
    totalStudentsIntake: int


class Branches(BaseModel):
    id: PyObjectId
    year: int = Field(gt=1900, lt=2100)
    branches: list[Students_Intake]
