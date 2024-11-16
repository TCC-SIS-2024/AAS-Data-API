from typing import Annotated, Any

from fastapi import APIRouter, Depends, Body, Request, Query
from fastapi.responses import JSONResponse

from src.application.usecases.create_permission import CreatePermissionUseCase
from src.application.usecases.find_all_permissions import FindAllPermissionsUseCase
from src.domain.entities.permission import PermissionInput
from src.web.dependencies import get_token, create_permission_use_case, get_all_permissions_use_case

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

@permissions_router.get(
    '/',
    summary="Route for fetching all permissions stored in System."
)
async def get_all_permissions(
        request: Request,
        use_case: Annotated[FindAllPermissionsUseCase, Depends(get_all_permissions_use_case)],
        search: Any = Query(None),
        page: int = Query(default=1),
        page_size: int = Query(default=10)
):
    """
    This Route is used to fetch all permissions stored in System.
    :param use_case:
    :param page_size:
    :param page:
    :param search: --> This parameter is used to search for a specific permission
    by its name value.

    :return: it returns a list of permissions stored in System.
    """

    response = await use_case.execute(page=page, page_size=page_size, search_input=search, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)