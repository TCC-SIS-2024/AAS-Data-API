from typing import Annotated, Any

from fastapi import APIRouter, Depends, Body, Request, Query, Path
from fastapi.responses import JSONResponse

from src.application.usecases.create_role import CreateRoleUseCase
from src.application.usecases.delete_role import DeleteRoleUseCase
from src.application.usecases.find_all_roles import FindAllRolesUseCase
from src.application.usecases.find_role_by_id import FindRoleByIdUseCase
from src.application.usecases.update_role_by_id import UpdateRoleByIdUseCase
from src.domain.entities.role import RoleInput
from src.web.dependencies import get_token, create_role_use_case, get_all_roles_use_case, find_role_by_id_use_case, \
    delete_role_by_id_use_case, update_role_by_id_use_case

roles_router = APIRouter(
    prefix="/roles",
    tags=["Roles users"],
    dependencies=[
        Depends(get_token)
    ]
)

@roles_router.post('/')
async def create_role(
        request: Request,
        role: Annotated[RoleInput, Body(...)],
        use_case: Annotated[CreateRoleUseCase, Depends(create_role_use_case)],
):
    """
    Route responsible for creating a role.
    :param role:
    :param use_case:
    :return:
    """

    response = await use_case.execute(role_input=role, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@roles_router.get(
    '/',
    summary="Route for fetching all roles stored in System."
)
async def get_all_roles(
        request: Request,
        use_case: Annotated[FindAllRolesUseCase, Depends(get_all_roles_use_case)],
        search: Any = Query(None),
        page: int = Query(default=1),
        page_size: int = Query(default=10)
):
    """
    This Route is used to fetch all roles stored in System.
    :param use_case:
    :param page_size:
    :param page:
    :param search: --> This parameter is used to search for a specific role by name.

    :return: it returns a list of role stored in System.
    """

    response = await use_case.execute(page=page, page_size=page_size, search_input=search, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@roles_router.get(
    '/{role_id}',
    summary="Route for finding role stored in System."
)
async def get_role_by_id(
        request: Request,
        role_id: Annotated[str, Path(...)],
        use_case: Annotated[FindRoleByIdUseCase, Depends(find_role_by_id_use_case)]
):
    response = await use_case.execute(role_id=role_id, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@roles_router.put(
    '/{role_id}',
    summary="Route for updating asset administration shells stored in System."
)
async def update_asset_administration_shells(
        request: Request,
        role_id: Annotated[str, Path(...)],
        role: Annotated[RoleInput, Body(...)],
        use_case: Annotated[UpdateRoleByIdUseCase, Depends(update_role_by_id_use_case)]
):
    response = await use_case.execute(role_input=role, role_id=role_id, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@roles_router.delete(
    '/{role_id}',
    summary="Route for deleting roles stored in System."
)
async def delete_role_by_id(
        request: Request,
        role_id: Annotated[str, Path(...)],
        use_case: Annotated[DeleteRoleUseCase, Depends(delete_role_by_id_use_case)],
):
    response = await use_case.execute(role_id=role_id, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)