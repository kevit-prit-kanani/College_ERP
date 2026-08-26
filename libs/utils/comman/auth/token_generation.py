import logging
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from libs.utils.comman.exceptions import AuthorizationError
from libs.utils.config import ALGORITHM, SECRET_KEY

bearer_scheme = HTTPBearer()

logger = logging.getLogger(__name__)


def create_access_token(user_id: str, role: str):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            raise AuthorizationError()
        # logger.info("Login: User=%s", payload)
        return payload

    except jwt.InvalidTokenError:
        raise AuthorizationError()


def require_roles(*allowed_roles: str):

    async def checker(
        current_user=Depends(get_current_user),
    ):

        if current_user["role"] not in allowed_roles:
            raise AuthorizationError(
                message=f"Required role: {', '.join(allowed_roles)}"
            )

        return current_user

    return checker


def check_email(db, email):
    response = db.find_one({"email": email})
    return bool(response)


def find_user(db, email):
    response = db.find_one({"email": email}, {"_id": 1, "role": 1})
    return response
