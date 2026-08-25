from fastapi import APIRouter

from apps.src.api.Student import student

api = APIRouter()
api.include_router(student)
