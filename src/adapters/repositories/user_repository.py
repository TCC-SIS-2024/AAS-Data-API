from src.domain.entities.user import UserOutput
from src.domain.interfaces.repositories import IUserRepository
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy import select, text
from src.infra.databases.pgdatabase import User


class UserRepository(IUserRepository):
    """ Class implementation for IUserRepository with all methods """

    def __init__(self, pg_engine: AsyncEngine):
        self.pg_engine: AsyncEngine = pg_engine

    async def find_by_email(self, email: str) -> UserOutput | None:
        """
        Implementation of abstract method `find_by_email` which will find a user by
        him/her email and return the data
        :param: email --> User email

        Equivalent SQL query:
        SELECT id, username, email ... FROM users WHERE email = :email
        """

        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            smtm = select(User).where(User.email == email)
            result = await session.execute(smtm)

            user = result.scalar_one_or_none()

            if user is not None:
                return UserOutput(**user.__dict__)

        return None
