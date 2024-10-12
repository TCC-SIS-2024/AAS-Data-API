from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from src.application.usecases.create_role import CreateRoleUseCase
from src.domain.entities.role import RoleInput
from src.web.dependencies import get_token, create_role_use_case

roles_router = APIRouter(
    prefix="/roles",
    tags=["Roles users"],
    dependencies=[
        Depends(get_token)
    ]
)

@roles_router.post('/')
async def create_role(
        role: Annotated[RoleInput, Body(...)],
        use_case: Annotated[CreateRoleUseCase, Depends(create_role_use_case)],
):
    """
    Route responsible for creating a role.
    :param role:
    :param use_case:
    :return:
    """

    response = await use_case.execute(role)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)