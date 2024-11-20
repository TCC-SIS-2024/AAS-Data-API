from traceback import print_exc
import json
from src.application.interfaces.usecase import UseCase
from src.domain.interfaces.repositories import IUserRepository
from src.web.http_helper import HttpHelper


class FindUserByIdUseCase(UseCase):
    """
    Use case for finding a user into system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IUserRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IUserRepository = repository

    async def execute(self, user_id: str):
        """
        This method will find the user into database.
        """
        try:

            if user_id is None or user_id == 'null':
                return HttpHelper.bad_request(Exception('User ID is required.'))

            user = await self.repository.find_by_id(user_id)

            if user is None:
                return HttpHelper.not_found(Exception('User not found.'))

            return HttpHelper.ok(json.loads(user.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))