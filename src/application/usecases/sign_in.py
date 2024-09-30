from src.application.interfaces.usecase import UseCase
from src.domain.entities.sign_in import SignIn
from src.domain.entities.user import UserOutput
from src.domain.interfaces.repositories import IUserRepository
from src.web.http_helper import HttpHelper, HttpResponse
from fastapi.security import OAuth2PasswordRequestForm
import json


class SignInUseCase(UseCase):
    """
    Use case for signing in a user onto the system. (Implementing the UseCase interface).
    """

    def __init__(self, repository: IUserRepository):
        """
        Constructor assigning the repository attribute as a dependency repository. (Dependency Injection by constructor).
        """
        self.repository: IUserRepository = repository

    async def execute(self, form_data: OAuth2PasswordRequestForm) -> HttpResponse:
        """
        This method will authenticate the user with provided data.
        :return: It returns a JWT access token
        """
        try:
            user = SignIn(email=form_data.username, password=form_data.password)
            user = await self.repository.find_by_email(user.email)

            if user is None:
                return HttpHelper.not_found(Exception('User not found!'))

            user = json.loads(user.model_dump_json())
            return HttpHelper.ok(user)
        except Exception as e:
            return HttpHelper.internal_server_error(Exception(e))