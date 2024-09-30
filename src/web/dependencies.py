from typing import Annotated
from fastapi import Depends
from src.adapters.repositories.user_repository import UserRepository
from src.application.usecases.sign_in import SignInUseCase
from src.infra.databases.pgdatabase import engine as postgres_engine
from sqlalchemy.ext.asyncio import AsyncEngine


def pg_engine() -> AsyncEngine:
    return postgres_engine

def user_repository(engine: Annotated[AsyncEngine, Depends(pg_engine)]):
    """
    function that injects the dependencies for UserRepository
    """

    return UserRepository(engine)

def sign_in_use_case(repository: Annotated[UserRepository, Depends(user_repository)]) -> SignInUseCase:
    """
    function that injects the dependencies for SignInUseCase
    """

    return SignInUseCase(repository)