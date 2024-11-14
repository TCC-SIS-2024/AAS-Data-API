from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.interfaces.repositories import IRoleRepository
from src.web.http_helper import HttpHelper


class FindRoleByIdUseCase(UseCase):
    """
    Use case for finding an role into system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IRoleRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IRoleRepository = repository

    async def execute(self, role_id: str):
        """
        This method will find the role into database.
        """
        try:

            if role_id is None or role_id == 'null':
                return HttpHelper.bad_request(Exception('Role ID is required.'))

            role = await self.repository.find_by_id(role_id)

            if role is None:
                return HttpHelper.not_found(Exception('Asset Administration Shell not found.'))

            return HttpHelper.ok(json.loads(role.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))