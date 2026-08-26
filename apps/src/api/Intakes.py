from fastapi import APIRouter, Depends

from libs.utils.comman.auth.token_generation import require_roles

intakes = APIRouter(
    tags=["Intakes"],
    dependencies=[Depends(require_roles("Admin"))],
)

# @intakes.get('/intakes')
# def get_all_intakes():
