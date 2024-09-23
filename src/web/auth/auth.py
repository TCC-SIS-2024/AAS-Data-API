from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(
    prefix="/auth"
)

@auth_router.post('/sign-in/')
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return 'ok'