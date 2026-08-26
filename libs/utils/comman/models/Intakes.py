from pydantic import BaseModel, Field

from libs.utils.comman.customs.variables import PyObjectId


class CreateIntake(BaseModel):
    department_id: PyObjectId
    totalStudentsIntake: int


class GetAllIntakes(CreateIntake):
    id: PyObjectId = Field()
    year: int = Field(gt=1900, lt=2100)

class UpdateIntake(CreateIntake):
    pass
