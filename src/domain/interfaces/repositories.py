from abc import ABC, abstractmethod

class IUserRepository(ABC):
    """
    Interface responsible for UserRepository main methods.
    """
    @abstractmethod
    async def find_by_email(self, email: str):
        """
        This abstract method is responsible for finding the user on the database and return him/her information.
        :param email:
        :return: a user information
        """
        raise NotImplemented()