from datetime import datetime
from traceback import print_exc

from src.application.interfaces.usecase import UseCase
from src.domain.interfaces.repositories import IAASHistoryData
from src.web.http_helper import HttpHelper


class GetAssetAdministrationShellHistoryDataUseCase(UseCase):
    """
    Use case for finding historical data from aas (opcua server). (Implementing the UseCase interface).
    """

    def __init__(self, repository: IAASHistoryData):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IAASHistoryData = repository

    async def execute(self, start_time: datetime, end_time: datetime, opcua_server_host: str, opcua_server_port: int):
        try:
            data, count = await self.repository.get_history_data_from_aas(start_time, end_time, opcua_server_host, opcua_server_port)
            return HttpHelper.ok({
                "data": data,
                "qtd": count
            })
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))