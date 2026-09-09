from libs.utils.comman.models.User import CreateUserRequest, UserResponse


class GetStudentResponse(UserResponse):
    enrollment_number: str
    batch: str
    semester: int
    admission_year: int


class CreateStudentRequest(CreateUserRequest):
    hash_password: str
    enrollment_number: str
    batch: str
    semester: int
    admission_year: int


class UpdateStudentRequest(CreateStudentRequest):
    pass
