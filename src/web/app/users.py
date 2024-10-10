from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.application.usecases.users_me import UsersMeUseCase
from src.web.dependencies import get_current_user_use_case, get_token

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@users_router.get('/me/', summary='Route for getting user information.')
async def get_user_info(
        token: Annotated[str, Depends(get_token)],
        use_case: Annotated[UsersMeUseCase, Depends(get_current_user_use_case)]
):
    """
    This method is used to get user information by a decorated Fast API route.
    :return:
    """

    response = await use_case.execute(token)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@users_router.get('/', summary='Route for getting user information.')
async def get_users(
        token: Annotated[str, Depends(get_token)],
        use_case: Annotated[UsersMeUseCase, Depends(get_current_user_use_case)]
):
    ...