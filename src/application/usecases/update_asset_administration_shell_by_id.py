from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.entities.asset_administration_shell import AssetAdministrationShellInput
from src.domain.interfaces.repositories import IAssetAdministrationShellRepository
from src.web.http_helper import HttpHelper


class UpdateAssetAdministrationShellByIdUseCase(UseCase):
    """
    Use case for update an aas onto the system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IAssetAdministrationShellRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IAssetAdministrationShellRepository = repository

    async def execute(self, aas_input: AssetAdministrationShellInput, aas_id: str):
        """
        This method will update the aas with provided data.
        """
        try:
            updated_aas = await self.repository.update_by_id(aas_input, aas_id)
            return HttpHelper.ok(json.loads(updated_aas.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))