from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.entities.role import RoleInput
from src.domain.interfaces.repositories import IRoleRepository
from src.web.http_helper import HttpHelper


class UpdateRoleByIdUseCase(UseCase):
    """
    Use case for update a role onto the system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IRoleRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IRoleRepository = repository

    async def execute(self, role_input: RoleInput, role_id: str):
        """
        This method will update the role with provided data.
        """
        try:
            updated_role = await self.repository.update_by_id(role_input, role_id)
            return HttpHelper.ok(json.loads(updated_role.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))