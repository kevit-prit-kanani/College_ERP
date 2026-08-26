from pydantic import BaseModel, Field

from libs.utils.comman.customs.variables import PyObjectId


class Intakes(BaseModel):
    id: PyObjectId = Field()
    year: int = Field(gt=1900, lt=2100)
    department_id: PyObjectId
    totalStudentsIntake: int
