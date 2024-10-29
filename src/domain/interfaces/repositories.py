from abc import ABC, abstractmethod
from typing import Optional, Any

from src.domain.entities.asset_administration_shell import AssetAdministrationShellInput
from src.domain.entities.permission import PermissionInput, PermissionOutput
from src.domain.entities.role import RoleInput, RoleOutput
from src.domain.entities.user import UserOutput, UserInput


class IUserRepository(ABC):
    """
    Interface responsible for UserRepository main methods.
    """

    @abstractmethod
    async def count_all_users(self):
        """
        This abstract method is responsible for counting all users on the database.
        :return: number of users
        """
        raise NotImplemented()

    @abstractmethod
    async def find_all(self, page: int, page_size: int):
        """
        This abstract method is responsible for finding all users on the database.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def find_by_email(self, email: str) -> UserOutput | None:
        """
        This abstract method is responsible for finding the user on the database and return him/her information.
        :param email:
        :return: a user information
        """
        raise NotImplemented()

    @abstractmethod
    async def create(self, user_input: UserInput) -> UserOutput | None:
        """
        This abstract method is responsible for storing the user on the database and return him/her information.
        :param user_input:
        :return: a user information
        """
        raise NotImplemented()

    @abstractmethod
    async def delete_all(self):
        """
        This abstract method is responsible for deleting all users on the database.
        """
        raise NotImplemented()

class IRoleRepository(ABC):
    """
    Interface responsible for RoleRepository main methods.
    """

    @abstractmethod
    async def create(self, role_input: RoleInput) -> RoleOutput:
        """
        This abstract method is responsible for storing the role on the database and return it information.
        :param role_input:
        :return: a role information
        """
        raise NotImplemented()

class IPermissionRepository(ABC):
    """
    Interface responsible for RoleRepository main methods.
    """

    @abstractmethod
    async def create(self, permission_input: PermissionInput) -> PermissionOutput:
        """
        This abstract method is responsible for storing the role on the database and return it information.
        :param permission_input:
        :return: a role information
        """
        raise NotImplemented()

class ISystemRepository(ABC):
    """
    Interface responsible for SystemRepository main methods.
    """

    @abstractmethod
    async def postgres_database_version(self):
        """
        This abstract method is responsible for getting the version of the PostgreSQL database.
        :return: version of the PostgreSQL database
        :return: version of current postgres database
        """
        raise NotImplemented()

    @abstractmethod
    async def postgres_max_connections(self):
        """
        This abstract method is responsible for getting the max connections of the PostgreSQL database.
        :return: max connections of the PostgreSQL database
        """
        raise NotImplemented()

    @abstractmethod
    async def postgres_opened_connections(self):
        """
        This abstract method is responsible for getting the opened connections of the PostgreSQL database.
        :return: opened connections of the PostgreSQL database
        """
        raise NotImplemented()

class IAssetAdministrationShellRepository(ABC):
    """
    Interface responsible for AssetAdministrationShellRepository main methods.
    """

    @abstractmethod
    async def find_by_id(self, aas_id: str):
        """
        This abstract method is responsible for finding the asset administration shell on the database and return it information.
        :param aas_id:
        :return: an asset administration shell information
        """
        raise NotImplemented()

    @abstractmethod
    async def update_by_id(self, aas: AssetAdministrationShellInput, aas_id: str):
        """
        This abstract method is responsible for updating the asset administration shell on the database and return it information.
        :param aas:
        :param aas_id:
        :return: an asset administration shell information
        """
        raise NotImplemented()

    @abstractmethod
    async def delete_by_id(self, aas_id: str):
        """
        This abstract method is responsible for deleting the asset administration shell on the database.
        """
        raise NotImplemented()

    @abstractmethod
    async def count_all_asset_administration_shells(self):
        """
        This abstract method is responsible for counting all asset administration shells on the database.
        :return: number of asset administration shells
        """
        raise NotImplemented()

    @abstractmethod
    async def find_all(self, page: int = 1, page_size: int = 10, search_input: Optional[Any] = None):
        """
        This abstract method is responsible for finding all asset administration shells on the database.
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    async def find_by_id_short(self, id_short: str):
        """
        This abstract method is responsible for finding the asset administration shell on the database and return it information.
        :param id_short:
        :return: an asset administration shell information
        """

        raise NotImplemented()

    @abstractmethod
    async def find_by_host(self, host: str):
        """
        This abstract method represents a method that call from database a AAS by host
        :param host:
        :return:
        """

        raise NotImplemented()

    @abstractmethod
    async def create(self, aas: AssetAdministrationShellInput):
        """
        This abstract method is responsible for storing the asset administration shell on the database and return it information.
        :param aas: AssetAdministrationShellInput:
        :return: a asset administration shell information
        """
        raise NotImplemented()