from fastapi import APIRouter, Depends

from src.web.dependencies import get_token

roles_router = APIRouter(
    prefix="/roles",
    tags=["Roles users"],
    dependencies=[
        Depends(get_token)
    ]
)

@roles_router.post('/')
async def create_role():
    ...