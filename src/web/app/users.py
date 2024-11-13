from typing import Annotated

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse

from src.application.usecases.find_all_users import FindAllUsersUseCase
from src.application.usecases.users_me import UsersMeUseCase
from src.web.dependencies import get_current_user_use_case, get_token, get_all_users_use_case

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

    response = await use_case.execute(page, page_size, request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)