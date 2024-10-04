import json
import traceback

from src.application.interfaces.usecase import UseCase
from src.domain.entities.user import UserInput, UserOutput
from src.domain.interfaces.encoders import IJwtEncoder
from src.domain.interfaces.repositories import IUserRepository
from src.web.http_helper import HttpHelper, HttpResponse


class SignUpUseCase(UseCase):
    """
    Use case for signing up in a user onto the system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IUserRepository, encoder: IJwtEncoder):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IUserRepository = repository
        self.encoder: IJwtEncoder = encoder

    async def execute(self, user_input: UserInput) -> HttpResponse:
        """
        This method will store the user with provided data.
        :return: user information
        """
        try:
            hashed_password = self.encoder.get_password_hash(user_input.password)
            user_input.password = hashed_password

            inserted_user: UserOutput = await self.repository.create(user_input)
            inserted_user = json.loads(inserted_user.model_dump_json())
            return HttpHelper.ok(inserted_user)

        except Exception as e:
            traceback.print_exc()
            return HttpHelper.internal_server_error(Exception(e))