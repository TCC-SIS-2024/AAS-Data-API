from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncEngine

from src.adapters.libs.bcrypt import BcryptAdapter
from src.adapters.repositories.asset_administration_shell_repository import AssetAdministrationShellRepository
from src.adapters.repositories.history_repository import AASHistoryRepository
from src.adapters.repositories.permission_repository import PermissionRepository
from src.adapters.repositories.role_repository import RoleRepository
from src.adapters.repositories.system_repository import SystemRepository
from src.adapters.repositories.user_repository import UserRepository
from src.application.usecases.create_asset_administration_shell import CreateAssetAdministrationShellUseCase
from src.application.usecases.create_permission import CreatePermissionUseCase
from src.application.usecases.create_role import CreateRoleUseCase
from src.application.usecases.delete_asset_administration_shell import DeleteAssetAdministrationShellUseCase
from src.application.usecases.delete_role import DeleteRoleUseCase
from src.application.usecases.find_all_asset_administration_shells import FindAllAssetAdministrationShellsUseCase
from src.application.usecases.find_all_roles import FindAllRolesUseCase
from src.application.usecases.find_all_users import FindAllUsersUseCase
from src.application.usecases.find_asset_administration_shell_by_id import FindAssetAdministrationShellByIdUseCase
from src.application.usecases.find_role_by_id import FindRoleByIdUseCase
from src.application.usecases.get_asset_administration_shell_history_data import \
    GetAssetAdministrationShellHistoryDataUseCase
from src.application.usecases.sign_in import SignInUseCase
from src.application.usecases.sign_up import SignUpUseCase
from src.application.usecases.system_status import SystemStatusUseCase
from src.application.usecases.update_asset_administration_shell_by_id import \
    UpdateAssetAdministrationShellByIdUseCase
from src.application.usecases.update_role_by_id import UpdateRoleByIdUseCase
from src.application.usecases.users_me import UsersMeUseCase
from src.infra.databases.pgdatabase import engine as postgres_engine
from src.web.decorators import PermissionDecorator


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

def aas_repository(engine: Annotated[AsyncEngine, Depends(pg_engine)]):
    """
    function that injects the dependencies for AssetAdministrationShellRepository
    """

    return AssetAdministrationShellRepository(engine)

def history_aas_data_repository():
    """
    function that injects the dependencies for AASHistoryRepository
    """

    return AASHistoryRepository()

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

def get_all_users_use_case(
        repository: Annotated[UserRepository, Depends(user_repository)]
):
    """
    function that injects the dependencies for findAllUsersUseCase
    """

    return PermissionDecorator(FindAllUsersUseCase(repository), 'user:read')

def get_all_aas_use_case(
        repository: Annotated[AssetAdministrationShellRepository, Depends(aas_repository)]
):
    """
    function that injects the dependencies for FindAllAssetAdministrationShellsUseCase
    """

    return PermissionDecorator(FindAllAssetAdministrationShellsUseCase(repository), 'aas:read')

def get_all_roles_use_case(
        repository: Annotated[RoleRepository, Depends(role_repository)]
):
    """
    function that injects the dependencies for FindAllRolesUseCase
    """

    return PermissionDecorator(FindAllRolesUseCase(repository), 'role:read')

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

    return PermissionDecorator(CreateRoleUseCase(repository), 'permission:read')

def create_aas_use_case(repository: Annotated[AssetAdministrationShellRepository, Depends(aas_repository)]):
    """
    function that injects the dependencies for CreateAssetAdministrationShellUseCase
    """

    return PermissionDecorator(CreateAssetAdministrationShellUseCase(repository), 'aas:create')

def delete_aas_use_case(repository: Annotated[AssetAdministrationShellRepository, Depends(aas_repository)]):
    """
    function that injects the dependencies for DeleteAssetAdministrationShellUseCase
    """

    return PermissionDecorator(DeleteAssetAdministrationShellUseCase(repository), 'aas:delete')

def find_aas_by_id_use_case(repository: Annotated[AssetAdministrationShellRepository, Depends(aas_repository)]):
    """
    function that injects the dependencies for FindAssetAdministrationShellByIdUseCase
    """

    return PermissionDecorator(FindAssetAdministrationShellByIdUseCase(repository), 'aas:read')

def update_aas_by_id_use_case(repository: Annotated[AssetAdministrationShellRepository, Depends(aas_repository)]):
    """
    function that injects the dependencies for UpdateAssetAdministrationShellByIdUseCase
    """

    return PermissionDecorator(UpdateAssetAdministrationShellByIdUseCase(repository), 'aas:update')

def create_permission_use_case(repository: Annotated[PermissionRepository, Depends(permission_repository)]):
    """
    function that injects the dependencies for CreatPermissionUseCase
    """

    return PermissionDecorator(CreatePermissionUseCase(repository), 'permission:create')

def find_role_by_id_use_case(repository: Annotated[RoleRepository, Depends(role_repository)]):
    """
    function that injects the dependencies for FindRoleByIdUseCase
    """

    return PermissionDecorator(FindRoleByIdUseCase(repository), 'role:read')

def delete_role_by_id_use_case(repository: Annotated[RoleRepository, Depends(role_repository)]):
    """
    function that injects the dependencies for DeleteRoleUseCase
    """

    return PermissionDecorator(DeleteRoleUseCase(repository), 'role:read')

def update_role_by_id_use_case(repository: Annotated[RoleRepository, Depends(role_repository)]):
    """
    function that injects the dependencies for UpdateRoleByIdUseCase
    """

    return PermissionDecorator(UpdateRoleByIdUseCase(repository), 'role:update')


def get_aas_history_data_use_case(repository: Annotated[AASHistoryRepository, Depends(history_aas_data_repository)]):
    """
    function that injects the dependencies for GetAssetAdministrationShellHistoryData
    """

    return PermissionDecorator(GetAssetAdministrationShellHistoryDataUseCase(repository), 'history:read')