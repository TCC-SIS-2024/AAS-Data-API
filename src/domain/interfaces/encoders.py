from abc import abstractmethod, ABC
from datetime import timedelta


class IJwtEncoder(ABC):
    """
    Interface responsible for JwtEncoder main methods.
    """
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        This method is responsible for verifying the password.
        :param plain_password: password received form the user.
        :param hashed_password: password stored in the database.
        :return: True if the password is correct, False otherwise.
        """

        raise NotImplementedError()

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        """

        :param password: Current password to be hashed.
        :return: Return the current password as hash.
        """

        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """
        This method is responsible for creating the access token.
        :param data: --> data to be encoded
        :param expires_delta: --> how many times the token will be valid
        :return: JWT access token
        """

        raise NotImplementedError()

    @abstractmethod
    def decode_jwt(self, token):
        """
        This method is responsible for decoding the jwt token.
        :param token: --> token to be decoded
        :return: decoded token
        """

        raise NotImplementedError()