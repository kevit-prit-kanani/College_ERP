"""Shared fixtures for API authentication integration tests."""

import os
from collections.abc import Generator
from copy import deepcopy
from typing import Any

# These must be set before importing the application because its settings are
# loaded at module import time. A localhost URI also prevents a developer's
# .env MongoDB URI from being used while the endpoint database handles are
# replaced with in-memory fakes below.
os.environ["SECRET_KEY"] = "pytest-only-secret-key-at-least-32"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017/college_erp_test"

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from apps.src.api import Student as student_api
from apps.src.auth import LoginAndRegister as auth_api
from libs.utils.comman.customs.HashPass import get_hashed_password
from libs.utils.db.mongodb import lifespan as lifespan_module
from main import app


class InMemoryCollection:
    """Small subset of the PyMongo collection API used by these routes."""

    def __init__(self, documents: list[dict[str, Any]]):
        self.documents = documents

    def find_one(
        self, query: dict[str, Any], projection: dict[str, int] | None = None
    ) -> dict[str, Any] | None:
        document = next(
            (
                candidate
                for candidate in self.documents
                if all(candidate.get(key) == value for key, value in query.items())
            ),
            None,
        )
        if document is None:
            return None

        result = deepcopy(document)
        if projection is None:
            return result

        included_fields = {key for key, include in projection.items() if include}
        if included_fields:
            result = {
                key: value for key, value in result.items() if key in included_fields
            }
        if projection.get("_id") == 0:
            result.pop("_id", None)
        return result

    def aggregate(self, pipeline: list[dict[str, Any]]):
        # The endpoint projects the exact public fields below. The fake starts
        # from documents that already represent that public projection.
        skip = next((stage["$skip"] for stage in pipeline if "$skip" in stage), 0)
        limit = next((stage["$limit"] for stage in pipeline if "$limit" in stage), None)
        records = deepcopy(self.documents)[skip:]
        return records if limit is None else records[:limit]

    def create_index(self, *args: Any, **kwargs: Any) -> str:
        return "test-index"


@pytest.fixture
def credentials() -> dict[str, str]:
    """Read the staff credentials supplied locally or by GitHub secrets."""
    email = os.getenv("TEST_STAFF_EMAIL")
    password = os.getenv("TEST_STAFF_PASSWORD")
    if not email or not password:
        pytest.fail(
            "Set TEST_STAFF_EMAIL and TEST_STAFF_PASSWORD before running API tests."
        )
    return {"email": email, "password": password, "role": "Staff"}


@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch, credentials: dict[str, str]
) -> Generator[TestClient, None, None]:
    staff = InMemoryCollection(
        [
            {
                "_id": ObjectId(),
                "email": credentials["email"],
                "hash_password": get_hashed_password(credentials["password"]),
                "role": "Staff",
            }
        ]
    )
    students = InMemoryCollection(
        [
            {
                "_id": ObjectId(),
                "first_name": "Asha",
                "last_name": "Patel",
                "email": "asha.patel@example.edu",
                "age": 20,
                "education": "B.Tech",
                "department_name": "Computer Science",
                "is_active": True,
                "is_deleted": False,
                "enrollment_number": "ERP-2026-001",
                "batch": "2026",
                "semester": 1,
                "admission_year": 2026,
            }
        ]
    )
    monkeypatch.setattr(auth_api, "db_Staff", staff)
    monkeypatch.setattr(student_api, "db_Student", students)
    monkeypatch.setattr(lifespan_module, "db_Intakes", InMemoryCollection([]))
    with TestClient(app) as api_client:
        yield api_client
