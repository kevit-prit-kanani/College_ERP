from fastapi import APIRouter, Depends

from libs.utils.comman.auth.token_generation import require_roles

department_admin = APIRouter(
    tags=["Department"],
    dependencies=[Depends(require_roles("Admin"))],
)
