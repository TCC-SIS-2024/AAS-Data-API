import traceback

from src.application.interfaces.usecase import UseCase
from src.domain.entities.system import SystemStatus, Dependencies, Database, PostgreSQL
from src.domain.interfaces.repositories import ISystemRepository
from src.web.http_helper import HttpHelper


class SystemStatusUseCase(UseCase):
    """
    Use case for getting the system status. (Implementing the UseCase interface).
    """

    def __init__(self, repository: ISystemRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository = repository

    async def execute(self):
        try:
            version = await self.repository.postgres_database_version()
            max_connections = await self.repository.postgres_max_connections()
            opened_connections = await self.repository.postgres_opened_connections()

            system_status = SystemStatus(
                dependencies=Dependencies(
                    databases=[
                        PostgreSQL(
                            version=version,
                            max_connections=max_connections,
                            opened_connections=opened_connections
                        )
                    ]
                )
            )

            return HttpHelper.ok(system_status)

        except Exception as e:
            traceback.print_exc()
            return HttpHelper.internal_server_error(Exception(e))
