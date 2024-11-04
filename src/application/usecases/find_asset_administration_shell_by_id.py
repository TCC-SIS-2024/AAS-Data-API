from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.entities.asset_administration_shell import AssetAdministrationShellInput
from src.domain.interfaces.repositories import IAssetAdministrationShellRepository
from src.web.http_helper import HttpHelper


class FindAssetAdministrationShellByIdUseCase(UseCase):
    """
    Use case for finding an aas into system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IAssetAdministrationShellRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IAssetAdministrationShellRepository = repository

    async def execute(self, aas_id: str):
        """
        This method will find the aas into database.
        """
        try:

            if aas_id is None:
                return HttpHelper.bad_request(Exception('Asset Administration Shell ID is required.'))

            aas = await self.repository.find_by_id(aas_id)

            if aas is None:
                return HttpHelper.not_found(Exception('Asset Administration Shell not found.'))

            return HttpHelper.ok(json.loads(aas.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))