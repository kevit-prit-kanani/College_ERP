from fastapi import APIRouter, Depends

from libs.utils.comman.auth.token_generation import require_roles

analytics = APIRouter(
    tags=["Analytics"],
    dependencies=[Depends(require_roles("Admin"))],
)
