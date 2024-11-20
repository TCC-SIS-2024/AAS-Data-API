from typing import Annotated

from fastapi import APIRouter, Depends, Request, Query, Body, Path
from fastapi.responses import JSONResponse

from src.application.usecases.create_user import CreateUserUseCase
from src.application.usecases.delete_user import DeleteUserUseCase
from src.application.usecases.find_all_users import FindAllUsersUseCase
from src.application.usecases.find_user_by_id import FindUserByIdUseCase
from src.application.usecases.users_me import UsersMeUseCase
from src.domain.entities.user import UserInput
from src.web.dependencies import get_current_user_use_case, get_token, get_all_users_use_case, create_user_use_case, \
    delete_aas_use_case, delete_user_use_case, find_user_by_id_use_case

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(get_token)
    ]
)

@users_router.get('/me/', summary='Route for getting user information.')
async def get_user_info(
        request: Request,
        use_case: Annotated[UsersMeUseCase, Depends(get_current_user_use_case)]
):
    """
    This method is used to get user information by a decorated Fast API route.
    :return:
    """
    token = request.headers['Authorization'].split(' ')[1]
    response = await use_case.execute(token)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@users_router.get('/', summary='Route for getting user information.')
async def get_users(
        request: Request,
        use_case: Annotated[FindAllUsersUseCase, Depends(get_all_users_use_case)],
        page: int = Query(default=1),
        page_size: int = Query(default=10),
):
    """
    This method is used to get user information by a decorated Fast API route.
    :param request:
    :param page_size:
    :param page:
    :param use_case:
    :return:
    """

    response = await use_case.execute(page=page, page_size=page_size, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@users_router.post('/', summary='Route for registering user in the System.')
async def create_user(
        request: Request,
        user_input: Annotated[UserInput, Body(...)],
        use_case: Annotated[CreateUserUseCase, Depends(create_user_use_case)]
):
    """
    This method is used to register user by a decorated Fast API route.
    :param user_input: user information to be stored.
    :param use_case: use case class for registration the user. (execute)
    :return:
    """

    response = await use_case.execute(user_input=user_input, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)


@users_router.delete(
    '/{user_id}',
    summary="Route for deleting users stored in System."
)
async def delete_user(
        request: Request,
        user_id: Annotated[str, Path(...)],
        use_case: Annotated[DeleteUserUseCase, Depends(delete_user_use_case)],
):
    response = await use_case.execute(user_id=user_id, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)


@users_router.get(
    '/{user_id}',
    summary="Route for finding users stored in System."
)
async def get_user_by_id(
        request: Request,
        user_id: Annotated[str, Path(...)],
        use_case: Annotated[FindUserByIdUseCase, Depends(find_user_by_id_use_case)]
):
    response = await use_case.execute(user_id=user_id, request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)