from typing import Annotated

from fastapi import APIRouter, Depends, Request

from src.web.dependencies import get_token

history_router = APIRouter(
    prefix="/histories",
    tags=["History Data"],
    dependencies=[
        Depends(get_token)
    ]
)

@history_router.get('/')
async def get_historized_data(request: Request):
    ...