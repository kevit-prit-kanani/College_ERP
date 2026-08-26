from fastapi import APIRouter, Depends

from libs.utils.comman.auth.token_generation import require_roles

branches = APIRouter(
    tags=['Branches'],
    dependencies=[Depends(require_roles("Admin"))],
)