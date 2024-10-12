from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.entities.permission import PermissionInput
from src.domain.interfaces.repositories import IPermissionRepository
from src.web.http_helper import HttpHelper


class CreatePermissionUseCase(UseCase):
    """
    Use case for creating a permission onto the system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IPermissionRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IPermissionRepository = repository

    async def execute(self, permission_input: PermissionInput):
        """
        This method will store the permission with provided data.
        """
        try:
            inserted_permission = await self.repository.create(permission_input)
            return HttpHelper.ok(json.loads(inserted_permission.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))