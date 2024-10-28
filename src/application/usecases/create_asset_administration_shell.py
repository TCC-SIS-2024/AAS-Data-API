from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.entities.asset_administration_shell import AssetAdministrationShellInput
from src.domain.interfaces.repositories import IAssetAdministrationShellRepository
from src.web.http_helper import HttpHelper


class CreateAssetAdministrationShellUseCase(UseCase):
    """
    Use case for creating an aas onto the system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IAssetAdministrationShellRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IAssetAdministrationShellRepository = repository

    async def execute(self, aas_input: AssetAdministrationShellInput):
        """
        This method will store the aas with provided data.
        """
        try:
            inserted_aas = await self.repository.create(aas_input)
            return HttpHelper.ok(json.loads(inserted_aas.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))