from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.interfaces.repositories import IPermissionRepository
from src.web.http_helper import HttpHelper


class FindPermissionByIdUseCase(UseCase):
    """
    Use case for finding an permission into system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IPermissionRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IPermissionRepository = repository

    async def execute(self, permission_id: str):
        """
        This method will find the permission into database.
        """
        try:

            if permission_id is None:
                return HttpHelper.bad_request(Exception('Permission ID is required.'))

            permission = await self.repository.find_by_id(permission_id)

            if permission is None:
                return HttpHelper.not_found(Exception('Permission not found.'))

            return HttpHelper.ok(json.loads(permission.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))