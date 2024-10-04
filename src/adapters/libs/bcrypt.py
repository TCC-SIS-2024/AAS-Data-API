import os
from datetime import datetime, timezone
from datetime import timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.domain.interfaces.encoders import IJwtEncoder


class BcryptAdapter(IJwtEncoder):
    """
    IJwtEncoder class implementation for Bcrypt encoding with all main methods.
    """

    pwd_context: CryptContext
    oauth2_scheme: OAuth2PasswordBearer

    def __init__(self):
        """
        Bcrypt class constructor with all necessary attributes.
        """
        self.pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        This method is responsible for verifying the password.
        :param plain_password: password received form the user.
        :param hashed_password: password stored in the database.
        :return: True if the password is correct, False otherwise.
        """

        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        This method is responsible for hashing the password.
        :param password: Current password to be hashed.
        :return: Return the current password as hash.
        """

        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """
        This method is responsible for creating the access token.
        :param data: --> data to be encoded
        :param expires_delta: --> how many times the token will be valid
        :return: JWT access token
        """

        to_encode: dict = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
        return encoded_jwt

    def decode_jwt(self, token):
        """
        This method is responsible for decoding the jwt token.
        :param token: --> token to be decoded
        :return: decoded token
        """

        return jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=[os.environ.get('ALGORITHM')])