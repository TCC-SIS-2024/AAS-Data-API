from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from src.web.dependencies import sign_in_use_case
from src.application.usecases.sign_in import SignInUseCase

auth_router = APIRouter(
    prefix="/auth"
)

@auth_router.post('/sign-in/', summary="Route for authenticating user in the System.")
async def sign_in(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        use_case: Annotated[SignInUseCase, Depends(sign_in_use_case)]):
    """
    This method is used to authenticate user by a decorated Fast API route.
    :param form_data: necessary information for authentication
    :param use_case: use case class for authentication the user. (execute
    :return:
    """
    response = await use_case.execute(form_data)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)
