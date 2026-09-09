import logging
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from libs.utils.comman.auth.token_generation import (
    check_email,
    create_access_token,
    find_user,
    get_current_user,
)
from libs.utils.comman.customs.HashPass import (
    get_hashed_password,
    verify_hashed_password,
)
from libs.utils.comman.customs.variables import PyObjectId
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
        raise HTTPException(
            status_code=404,
            detail="Email Not Found",
        )

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

    token = create_access_token(user_id=str(user.id), role=user.role)
    response = Token(access_token=token, token_type="JWT", role=user.role)
    return response


@auth.get("/decode-token")
async def get_current_user_details(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Return the decoded token claims and the authenticated user's profile."""
    user_id = PyObjectId(current_user["sub"])
    role = current_user["role"]

    if role == "Student":
        user = db_Student.find_one({"_id": user_id})
    elif role in {"Staff", "Admin"}:
        user = db_Staff.find_one({"_id": user_id})
    else:
        raise AuthenticationError("Unsupported user role in token")

    logger.info(
        {
            "token": current_user,
            "role": role,
            "roles": [role],
            "user": user,
        }
    )
    if user is None:
        raise NotFoundError("User", current_user["sub"])
    return {"token": current_user, "role": role, "roles": [role]}


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
