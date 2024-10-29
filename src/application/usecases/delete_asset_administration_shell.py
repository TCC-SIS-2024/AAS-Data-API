from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.entities.asset_administration_shell import AssetAdministrationShellInput
from src.domain.interfaces.repositories import IAssetAdministrationShellRepository
from src.web.http_helper import HttpHelper


class DeleteAssetAdministrationShellUseCase(UseCase):
    """
    Use case for deleting an aas from system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IAssetAdministrationShellRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IAssetAdministrationShellRepository = repository

    async def execute(self, aas_id: str):
        """
        This method will delete the aas from database.
        """
        try:
            deleted_aas_id = await self.repository.delete_by_id(aas_id)

            response_msg = {
                "aas_id": str(deleted_aas_id),
                "message": "Asset Administration Shell deleted successfully."
            }

            if deleted_aas_id is not None:
                return HttpHelper.ok(response_msg)
            else:
                return HttpHelper.bad_request(Exception('Not possible to delete Asset Administration Shell.'))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))