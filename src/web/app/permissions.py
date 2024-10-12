from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from src.application.usecases.create_permission import CreatePermissionUseCase
from src.domain.entities.permission import PermissionInput
from src.web.dependencies import get_token, create_permission_use_case

permissions_router = APIRouter(
    prefix="/permissions",
    tags=["Permission users' permission"],
    dependencies=[
        Depends(get_token)
    ]
)

@permissions_router.post('/')
async def create_permission(
        permission: Annotated[PermissionInput, Body(...)],
        use_case: Annotated[CreatePermissionUseCase, Depends(create_permission_use_case)],
):
    """
    Route responsible for creating a permission.
    :param permission:
    :param use_case:
    :return:
    """

    response = await use_case.execute(permission)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)