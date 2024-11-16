import json
from traceback import print_exc
from typing import Optional, Any

from src.application.interfaces.usecase import UseCase
from src.domain.entities.pagination import PaginationResponse
from src.domain.interfaces.repositories import IPermissionRepository
from src.web.http_helper import HttpHelper


class FindAllPermissionsUseCase(UseCase):
    """
    Use case for getting all permissions' information. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IPermissionRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """

        self.repository: IPermissionRepository = repository

    async def execute(self, page: int = 1, page_size: int = 10, search_input: Optional[Any] = None):
        """
        This method will get all permissions' information.
        """
        try:
            permissions = await self.repository.find_all(page, page_size, search_input)
            total_qtd_permissions = await self.repository.count_permissions()

            pagination_response = PaginationResponse(data=permissions, total=total_qtd_permissions)
            return HttpHelper.ok(json.loads(pagination_response.model_dump_json()))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))