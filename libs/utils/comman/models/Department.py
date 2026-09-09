from libs.utils.comman.customs.variables import MongoBaseModel, PyObjectId


class GetAllDepartment(MongoBaseModel):

    id: PyObjectId
    name: str
