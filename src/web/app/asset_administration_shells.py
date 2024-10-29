from typing import Annotated, Any

from fastapi import APIRouter, Query, Depends, Body, Path
from fastapi.responses import JSONResponse

from src.application.usecases.create_asset_administration_shell import CreateAssetAdministrationShellUseCase
from src.application.usecases.delete_asset_administration_shell import DeleteAssetAdministrationShellUseCase
from src.application.usecases.find_all_asset_administration_shells import FindAllAssetAdministrationShellsUseCase
from src.application.usecases.find_asset_administration_shell_by_id import FindAssetAdministrationShellByIdUseCase
from src.domain.entities.asset_administration_shell import AssetAdministrationShellInput
from src.web.dependencies import get_token, create_aas_use_case, get_all_aas_use_case, delete_aas_use_case, \
    find_aas_by_id_use_case

asset_administration_shells_router = APIRouter(
    prefix="/asset-administration-shells",
    tags=["Asset Administration Shells"],
    dependencies=[
        Depends(get_token)
    ]
)

@asset_administration_shells_router.get(
    '/',
    summary="Route for fetching all asset administration shells stored in System."
)
async def get_asset_administration_shells(
        use_case: Annotated[FindAllAssetAdministrationShellsUseCase, Depends(get_all_aas_use_case)],
        search: Any = Query(None),
        page: int = Query(default=1),
        page_size: int = Query(default=10)
):
    """
    This Route is used to fetch all asset administration shells stored in System.
    :param use_case: 
    :param page_size:
    :param page:
    :param search: --> This parameter is used to search for a specific asset administration shell
    by its IdShort or Hostname.

    :return: it returns a list of asset administration shells stored in System.
    """

    response = await use_case.execute(page, page_size, search)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@asset_administration_shells_router.post(
    '/',
    summary="Route for storing asset administration shells stored in System."
)
async def create_asset_administration_shells(
        use_case: Annotated[CreateAssetAdministrationShellUseCase, Depends(create_aas_use_case)],
        aas: Annotated[AssetAdministrationShellInput, Body(...)],
):
    response = await use_case.execute(aas)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@asset_administration_shells_router.patch(
    '/',
    summary="Route for updating a piece of asset administration shells stored in System."
)
async def get_asset_administration_shells(
        search: str = Query(None)
):
    ...

@asset_administration_shells_router.put(
    '/',
    summary="Route for updating asset administration shells stored in System."
)
async def get_asset_administration_shells(
        search: str = Query(None)
):
    ...

@asset_administration_shells_router.delete(
    '/{aas_id}',
    summary="Route for deleting asset administration shells stored in System."
)
async def get_asset_administration_shells(
        aas_id: Annotated[str, Path(...)],
        use_case: Annotated[DeleteAssetAdministrationShellUseCase, Depends(delete_aas_use_case)],
):
    response = await use_case.execute(aas_id)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)

@asset_administration_shells_router.get(
    '/{aas_id}',
    summary="Route for finding asset administration shells stored in System."
)
async def get_asset_administration_shell_by_id(
        aas_id: Annotated[str, Path(...)],
        use_case: Annotated[FindAssetAdministrationShellByIdUseCase, Depends(find_aas_by_id_use_case)]
):
    response = await use_case.execute(aas_id)
    return JSONResponse(content=response.model_dump(), status_code=response.status_code)