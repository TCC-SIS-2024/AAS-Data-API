from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
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
    request: Request,
    use_case: Annotated[GetAssetAdministrationShellHistoryDataUseCase, Depends(get_aas_history_data_use_case)],
    opcua_server_host: Annotated[str, Query(...)],
    opcua_server_port: Annotated[int, Query(...)],
    start_date: Annotated[datetime, Query(...)],
    end_date: datetime = Query(default=datetime.now(timezone.utc))
):
    """
    Route responsible for getting historized data from aas.
    :return:
    """

    response = await use_case.execute(
        start_time=start_date,
        end_time=end_date,
        opcua_server_host=opcua_server_host,
        opcua_server_port=opcua_server_port,
        request=request)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)