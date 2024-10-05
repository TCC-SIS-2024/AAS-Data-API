import traceback

from fastapi.security import OAuth2PasswordRequestForm
from pydantic_core import ValidationError
from src.application.interfaces.usecase import UseCase
from src.domain.entities.sign_in import SignIn, SignInFields
from src.domain.entities.user import UserOutput
from src.domain.interfaces.repositories import IUserRepository
from src.web.http_helper import HttpHelper, HttpResponse


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

            fields = SignInFields(email=form_data.username, password=form_data.password)
            sign_in = SignIn(fields.email, fields.password)

            user: UserOutput = await self.repository.find_by_email(sign_in.email)

            if user is None:
                return HttpHelper.not_found(Exception('User not found!'))

            authenticated: bool = sign_in.authenticate(form_data.password, user)

            if not authenticated:
                return HttpHelper.unauthorized(Exception('Invalid credentials'))

            token: dict = sign_in.generate_access_token(user)

            return HttpHelper.ok(token)
        except ValidationError as e:
            return HttpHelper.unprocessable_entity(Exception(e))
        except Exception as e:
            return HttpHelper.internal_server_error(Exception(e))