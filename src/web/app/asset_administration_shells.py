from fastapi import APIRouter, Query, Depends

from src.web.dependencies import get_token

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
        search: str = Query(None)
):
    """
    This Route is used to fetch all asset administration shells stored in System.
    :param search: --> This parameter is used to search for a specific asset administration shell
    by its IdShort or Hostname.

    :return: it returns a list of asset administration shells stored in System.
    """

    return [
        {
            "id_short": "AAS1",
            "host": "192.168.100.22",
            "port": 4849,
            "database_endpoint": "0.0.0.0",
            "aas_modeling": "modeling.json",
            "active": True
        }
    ]

@asset_administration_shells_router.post(
    '/',
    summary="Route for storing asset administration shells stored in System."
)
async def get_asset_administration_shells(
        search: str = Query(None)
):
    ...

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
    '/',
    summary="Route for deleting asset administration shells stored in System."
)
async def get_asset_administration_shells(
        search: str = Query(None)
):
    ...