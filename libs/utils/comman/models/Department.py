from pydantic import BaseModel, ConfigDict, Field

from libs.utils.comman.customs.variables import PyObjectId


class GetAllDepartment(BaseModel):
    model_config = ConfigDict(use_bson=True)

    id: PyObjectId = Field(alias="_id")
    name: str
