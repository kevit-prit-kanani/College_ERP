from pydantic import BaseModel, ConfigDict

from libs.utils.comman.customs.variables import PyObjectId


class Department(BaseModel):
    model_config = ConfigDict(use_bson=True)

    id: PyObjectId | None
    name: str
