from bson import ObjectId
from pydantic import BaseModel, Field


class Students_Intake(BaseModel):
    name: str
    totalStudentsIntake: int

class Branches(BaseModel):
    year: int = Field(gt=1900, lt=2100)
    branches: list[Students_Intake]