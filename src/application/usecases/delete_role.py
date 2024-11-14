from traceback import print_exc
from src.application.interfaces.usecase import UseCase
from src.domain.interfaces.repositories import IRoleRepository
from src.web.http_helper import HttpHelper


class DeleteRoleUseCase(UseCase):
    """
    Use case for deleting an role from system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IRoleRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IRoleRepository = repository

    async def execute(self, role_id: str):
        """
        This method will delete the role from database.
        """
        try:

            role = await self.repository.find_by_id(role_id)

            if role is None:
                return HttpHelper.not_found(Exception('Role not found.'))

            deleted_role_id = await self.repository.delete_by_id(role_id)

            response_msg = {
                "role_id": str(deleted_role_id),
                "message": "Role deleted successfully."
            }

            if deleted_role_id is not None:
                return HttpHelper.ok(response_msg)
            else:
                return HttpHelper.bad_request(Exception('Not possible to delete Role.'))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))