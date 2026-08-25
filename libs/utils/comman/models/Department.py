from bson import ObjectId
from pydantic import BaseModel, ConfigDict


class Department(BaseModel):
    model_config = ConfigDict(use_bson=True)
    
    id: ObjectId | None
    name: str