from traceback import print_exc
from src.application.interfaces.usecase import UseCase
from src.domain.interfaces.repositories import IUserRepository
from src.web.http_helper import HttpHelper


class DeleteUserUseCase(UseCase):
    """
    Use case for deleting a user from system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IUserRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IUserRepository = repository

    async def execute(self, user_id: str):
        """
        This method will delete the user from database.
        """
        try:

            user = await self.repository.find_by_id(user_id)

            if user is None:
                return HttpHelper.not_found(Exception('User not found.'))

            deleted_user_id = await self.repository.delete_by_id(user_id)

            response_msg = {
                "user_id": str(deleted_user_id),
                "message": "User deleted successfully."
            }

            if deleted_user_id is not None:
                return HttpHelper.ok(response_msg)
            else:
                return HttpHelper.bad_request(Exception('Not possible to delete User.'))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))