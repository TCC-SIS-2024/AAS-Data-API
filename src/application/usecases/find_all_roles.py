import json
from traceback import print_exc
from typing import Optional, Any

from src.application.interfaces.usecase import UseCase
from src.domain.entities.pagination import PaginationResponse
from src.domain.interfaces.repositories import IRoleRepository
from src.web.http_helper import HttpHelper


class FindAllRolesUseCase(UseCase):
    """
    Use case for getting all roles' information. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IRoleRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """

        self.repository: IRoleRepository = repository

    async def execute(self, page: int = 1, page_size: int = 10, search_input: Optional[Any] = None):
        """
        This method will get all roles' information.
        """
        try:
            roles = await self.repository.find_all(page, page_size, search_input)
            total_qtd_roles = await self.repository.count_roles()

            pagination_response = PaginationResponse(data=roles, total=total_qtd_roles)
            return HttpHelper.ok(json.loads(pagination_response.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))