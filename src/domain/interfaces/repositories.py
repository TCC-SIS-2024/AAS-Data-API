from abc import ABC, abstractmethod

from src.domain.entities.permission import PermissionInput, PermissionOutput
from src.domain.entities.role import RoleInput, RoleOutput
from src.domain.entities.user import UserOutput, UserInput


class IUserRepository(ABC):
    """
    Interface responsible for UserRepository main methods.
    """
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