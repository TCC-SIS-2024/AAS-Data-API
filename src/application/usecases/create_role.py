from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.entities.role import RoleInput
from src.domain.interfaces.repositories import IRoleRepository
from src.web.http_helper import HttpHelper


class CreateRoleUseCase(UseCase):
    """
    Use case for creating a role onto the system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IRoleRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IRoleRepository = repository

    async def execute(self, role_input: RoleInput):
        """
        This method will store the role with provided data.
        """
        try:
            inserted_role = await self.repository.create(role_input)
            return HttpHelper.ok(json.loads(inserted_role.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))