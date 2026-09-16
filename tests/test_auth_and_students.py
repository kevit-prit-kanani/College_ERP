"""End-to-end tests for staff login and the protected student-list endpoint."""

import jwt
from fastapi.testclient import TestClient

from libs.utils.comman.models.Auth import Token
from libs.utils.config import ALGORITHM, SECRET_KEY


def login(client: TestClient, credentials: dict[str, str]) -> dict[str, str]:
    response = client.post("/auth/login", json=credentials)
    assert response.status_code == 200, response.text
    return response.json()


def test_staff_login_returns_a_valid_token(
    client: TestClient, credentials: dict[str, str]
) -> None:
    """The supplied staff account receives a JWT response matching Token."""
    body = login(client, credentials)
    token_response = Token.model_validate(body)

    assert token_response.access_token
    assert token_response.token_type == "JWT"
    assert token_response.role == "Staff"
    assert token_response.user_id

    claims = jwt.decode(body["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert claims["sub"] == body["user_id"]
    assert claims["role"] == "Staff"


def test_staff_token_can_get_the_student_list(
    client: TestClient, credentials: dict[str, str]
) -> None:
    """A token returned by login authorizes GET /students."""
    token = login(client, credentials)["access_token"]

    response = client.get("/students", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200, response.text
    students = response.json()
    assert isinstance(students, list)
    assert students
    assert students[0]["enrollment_number"] == "ERP-2026-001"


def test_student_list_rejects_a_request_without_a_token(client: TestClient) -> None:
    """The student list remains protected when no bearer token is supplied."""
    response = client.get("/students")

    assert response.status_code == 401
