import json
from traceback import print_exc
from jwt.exceptions import InvalidTokenError
from src.application.interfaces.usecase import UseCase
from src.domain.entities.user import UserOutput
from src.domain.interfaces.encoders import IJwtEncoder
from src.domain.interfaces.repositories import IUserRepository
from src.web.http_helper import HttpHelper


class UsersMeUseCase(UseCase):
    """
    Use case for getting user information. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IUserRepository, encoder: IJwtEncoder):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """

        self.repository: IUserRepository = repository
        self.encoder: IJwtEncoder = encoder

    async def execute(self, token: str):
        """
        This method will get the current user information.
        """
        try:
            payload = self.encoder.decode_jwt(token)
            user_email: str = payload.get('sub')
            user_information: UserOutput = await self.repository.find_by_email(user_email)
            user_information: dict = json.loads(user_information.model_dump_json())
            return HttpHelper.ok(user_information)
        except InvalidTokenError as e:
            print_exc()
            return HttpHelper.unauthorized(Exception(e))
        except Exception as e:
            print_exc()
            return HttpHelper.internal_server_error(Exception(e))