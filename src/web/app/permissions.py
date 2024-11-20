from typing import Annotated, Any

from fastapi import APIRouter, Depends, Body, Request, Query, Path
from fastapi.responses import JSONResponse

from src.application.usecases.create_permission import CreatePermissionUseCase
from src.application.usecases.find_all_permissions import FindAllPermissionsUseCase
from src.application.usecases.find_permission_id import FindPermissionByIdUseCase
from src.domain.entities.permission import PermissionInput
from src.web.dependencies import get_token, create_permission_use_case, get_all_permissions_use_case, \
    find_permission_by_id_use_case

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

@permissions_router.get(
    '/{permission_id}',
    summary="Route for finding permissions stored in System."
)
async def get_asset_administration_shell_by_id(
        request: Request,
        permission_id: Annotated[str, Path(...)],
        use_case: Annotated[FindPermissionByIdUseCase, Depends(find_permission_by_id_use_case)]
):
    response = await use_case.execute(permission_id=permission_id, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)