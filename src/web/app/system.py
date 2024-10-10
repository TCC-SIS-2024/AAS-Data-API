from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.application.usecases.system_status import SystemStatusUseCase
from src.web.dependencies import system_use_case, get_token

system_router = APIRouter(
    prefix="/system",
    tags=["Health System"],
    dependencies=[
        Depends(get_token)
    ]
)

@system_router.get('/status/', summary='Route for getting system status.')
async def get_system_status(
        use_case: Annotated[SystemStatusUseCase, Depends(system_use_case)]
):
    """
    Route responsible for getting the system status. Such as database health, max connections, etc.
    :return:
    """

    response = await use_case.execute()
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)