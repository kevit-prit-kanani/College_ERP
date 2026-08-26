from fastapi import APIRouter

from apps.src.api.Department import department_admin
from apps.src.api.Staff import staff, staff_admin
from apps.src.api.Student import student_admin_staff, student_all_roles
from apps.src.auth.LoginAndRegister import auth

api = APIRouter()
api.include_router(auth)
api.include_router(student_all_roles)
api.include_router(student_admin_staff)
api.include_router(staff)
api.include_router(staff_admin)
api.include_router(department_admin)
