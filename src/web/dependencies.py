from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncEngine

from src.adapters.libs.bcrypt import BcryptAdapter
from src.adapters.repositories.permission_repository import PermissionRepository
from src.adapters.repositories.role_repository import RoleRepository
from src.adapters.repositories.system_repository import SystemRepository
from src.adapters.repositories.user_repository import UserRepository
from src.application.usecases.create_permission import CreatePermissionUseCase
from src.application.usecases.create_role import CreateRoleUseCase
from src.application.usecases.sign_in import SignInUseCase
from src.application.usecases.sign_up import SignUpUseCase
from src.application.usecases.system_status import SystemStatusUseCase
from src.application.usecases.users_me import UsersMeUseCase
from src.infra.databases.pgdatabase import engine as postgres_engine


def pg_engine() -> AsyncEngine:
    return postgres_engine


def system_repository(engine: Annotated[AsyncEngine, Depends(pg_engine)]):
    """
    function that injects the dependencies for SystemRepository
    """

    return SystemRepository(engine)

def user_repository(engine: Annotated[AsyncEngine, Depends(pg_engine)]):
    """
    function that injects the dependencies for UserRepository
    """

    return UserRepository(engine)

def role_repository(engine: Annotated[AsyncEngine, Depends(pg_engine)]):
    """
    function that injects the dependencies for RoleRepository
    """

    return RoleRepository(engine)

def permission_repository(engine: Annotated[AsyncEngine, Depends(pg_engine)]):
    """
    function that injects the dependencies for PermissionRepository
    """

    return PermissionRepository(engine)

def jwt_encoder() -> BcryptAdapter:
    """
    function that injects the dependencies for JwtEncoder
    """

    return BcryptAdapter()

def get_token(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/sign-in/"))],
) -> str:
    """
    function that injects the dependencies for token
    """

    return token


def get_current_user_use_case(
        repository: Annotated[UserRepository, Depends(user_repository)],
        encoder: Annotated[BcryptAdapter, Depends(jwt_encoder)]
):
    """
    function that injects the dependencies for GetCurrentUserUseCase
    """

    return UsersMeUseCase(repository, encoder)

def sign_in_use_case(repository: Annotated[UserRepository, Depends(user_repository)]) -> SignInUseCase:
    """
    function that injects the dependencies for SignInUseCase
    """

    return SignInUseCase(repository)

def sign_up_use_case(
        repository: Annotated[UserRepository, Depends(user_repository)],
        encoder: Annotated[BcryptAdapter, Depends(jwt_encoder)],
) -> SignUpUseCase:
    """
    function that injects the dependencies for SignUpUseCase
    """

    return SignUpUseCase(repository, encoder)

def system_use_case(repository: Annotated[SystemRepository, Depends(system_repository)]):
    """
    function that injects the dependencies for SystemUseCase
    """

    return SystemStatusUseCase(repository)

def create_role_use_case(repository: Annotated[RoleRepository, Depends(role_repository)]):
    """
    function that injects the dependencies for CreateRoleUseCase
    """

    return CreateRoleUseCase(repository)

def create_permission_use_case(repository: Annotated[PermissionRepository, Depends(permission_repository)]):
    """
    function that injects the dependencies for CreatPermissionUseCase
    """

    return CreatePermissionUseCase(repository)