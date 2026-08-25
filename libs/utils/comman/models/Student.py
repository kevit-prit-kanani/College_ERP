from libs.utils.comman.models.User import CreateUserRequest, UserResponse


class GetStudentResponse(UserResponse):
    enrollment_number: str
    batch: str
    semester: int


class CreateStudentRequest(CreateUserRequest):
    enrollment_number: str
    batch: str
    semester: int
