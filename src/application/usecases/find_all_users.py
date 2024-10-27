import json
from traceback import print_exc
from jwt.exceptions import InvalidTokenError
from src.application.interfaces.usecase import UseCase
from src.domain.entities.pagination import PaginationResponse
from src.domain.entities.user import UserOutput
from src.domain.interfaces.encoders import IJwtEncoder
from src.domain.interfaces.repositories import IUserRepository
from src.web.http_helper import HttpHelper


class FindAllUsersUseCase(UseCase):
    """
    Use case for getting all users' information. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IUserRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """

        self.repository: IUserRepository = repository

    async def execute(self, page: int = 1, page_size: int = 10):
        """
        This method will get all users' information.
        """
        try:
            users = await self.repository.find_all(page, page_size)
            total_qtd_users = await self.repository.count_all_users()

            pagination_response = PaginationResponse(data=users, total=total_qtd_users)

            return HttpHelper.ok(json.loads(pagination_response.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))