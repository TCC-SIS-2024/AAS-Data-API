from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from src.application.usecases.get_asset_administration_shell_history_data import \
    GetAssetAdministrationShellHistoryDataUseCase
from src.web.dependencies import get_token, get_aas_history_data_use_case

history_router = APIRouter(
    prefix="/histories",
    tags=["History Data"],
    dependencies=[
        Depends(get_token)
    ]
)

@history_router.get('/')
async def get_historized_data(
    use_case: Annotated[GetAssetAdministrationShellHistoryDataUseCase, Depends(get_aas_history_data_use_case)],
    start_date: Annotated[datetime, Query(...)],
    end_date: Annotated[datetime, Query(...)]
):
    """
    Route responsible for getting historized data from aas.
    :return:
    """

    response = await use_case.execute(start_date, end_date)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)