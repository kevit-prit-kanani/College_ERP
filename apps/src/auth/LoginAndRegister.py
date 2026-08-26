import logging
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException

from libs.utils.comman.auth.token_generation import (
    check_email,
    create_access_token,
    find_user,
)
from libs.utils.comman.customs.HashPass import (
    get_hashed_password,
    verify_hashed_password,
)
from libs.utils.comman.exceptions import AuthenticationError, NotFoundError
from libs.utils.comman.models.APIResponse import DBResponse, InsertEffect
from libs.utils.comman.models.Auth import LoginRequest, StaffRegisterRequest, Token
from libs.utils.db.mongodb import db_Staff, db_Student

auth = APIRouter(prefix="/auth", tags=["Auth"])

logger = logging.getLogger(__name__)


@auth.post("/login")
async def login(login_request: LoginRequest) -> Token:
    if (
        (login_request.role == "Staff")
        and not check_email(db_Staff, login_request.email)
    ) or (
        login_request.role == "Student"
        and not check_email(db_Student, login_request.email)
    ):
        raise NotFoundError(status_code=404, detail="Email Not Found")

    if login_request.role == "Staff":
        db = db_Staff
    elif login_request.role == "Student":
        db = db_Student

    hash_pass_obj = db.find_one(
        {"email": login_request.email}, {"hash_password": 1, "_id": 0}
    )
    hashed_password = hash_pass_obj["hash_password"]

    if not verify_hashed_password(login_request.password, hashed_password):
        raise AuthenticationError(message="password dose not match, Try again!")

    user = find_user(db, login_request.email)

    id = str(user["_id"])
    if not user["role"]:
        role = "Admin"
    else:
        role = str(user["role"])

    token = create_access_token(user_id=id, role=role)
    response = Token(access_token=token, token_type="JWT")
    return response


@auth.post("/register/staff")
async def staff_register(create_staff_request: StaffRegisterRequest) -> DBResponse:
    existing_staff = db_Staff.find_one({"email": create_staff_request.email})
    if existing_staff:
        raise HTTPException(status_code=400, detail="Email already registered")

    hash_password = get_hashed_password(create_staff_request.password)
    new_staff = create_staff_request.model_dump()
    if new_staff["password"]:
        new_staff.pop("password")
    new_staff.update(
        {
            "is_active": True,
            "is_deleted": False,
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "hash_password": hash_password,
        }
    )

    result = db_Staff.insert_one(new_staff)
    response = DBResponse(
        id=result.inserted_id,
        total_records=InsertEffect(created_count=1),
        items=[],
        message="Staff Registered successfully",
    )
    return response
