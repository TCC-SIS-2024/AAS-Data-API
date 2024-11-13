from typing import Annotated, Any

from fastapi import APIRouter, Depends, Body, Request, Query
from fastapi.responses import JSONResponse

from src.application.usecases.create_role import CreateRoleUseCase
from src.application.usecases.find_all_roles import FindAllRolesUseCase
from src.domain.entities.role import RoleInput
from src.web.dependencies import get_token, create_role_use_case, get_all_roles_use_case

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