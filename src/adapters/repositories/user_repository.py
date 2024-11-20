from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from src.domain.entities.user import UserOutput, UserInput
from src.domain.interfaces.repositories import IUserRepository
from src.infra.databases.pgdatabase import User, Role
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload


class UserRepository(IUserRepository):
    """ Class implementation for IUserRepository with all methods """

    def __init__(self, pg_engine: AsyncEngine):
        self.pg_engine: AsyncEngine = pg_engine

    async def count_all_users(self):
        """
        Implementation of abstract method `count_all_users` which will count all users
        :return: number of users fetched in database
        """

        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            smtm = select(User)
            result = await session.execute(smtm)
            users_qtd = len(result.scalars().fetchall())
            return users_qtd

        return None

    async def find_all(self, page: int = 1, page_size: int = 10):
        """
        Implementation of abstract method `find_all` which will find all users
        :return:  fetched in database
        """

        session = async_sessionmaker(self.pg_engine)

        async with session() as session:

            offset = (page - 1) * page_size

            smtm = select(User).options(
                joinedload(User.role).options(joinedload(Role.permissions))
            ).limit(page_size).offset(offset)

            result = await session.execute(smtm)
            fetched_users = result.unique().scalars()
            users: List[UserOutput] = []

            for user in fetched_users.fetchall():
                encoded = jsonable_encoder(user)
                users.append(UserOutput(**encoded))

            return users

        return None


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
            smtm = select(User).options(joinedload(User.role).options(joinedload(Role.permissions))).where(User.email == email)
            result = await session.execute(smtm)

            user = result.unique().scalar_one_or_none()

            encoded = jsonable_encoder(user)

            if user is not None:
                return UserOutput(**encoded)

        return None

    async def create(self, user_base: UserInput) -> UserOutput | None:
        """
        Implementation of abstract method `create` which will store a user by
        :param user_base: --> User information
        """

        try:
            session = async_sessionmaker(self.pg_engine, autoflush=False)
            async with session() as session:
                smtm = insert(User).values(
                    username=user_base.username,
                    email=user_base.email,
                    password=user_base.password,
                    role_id=user_base.role_id
                ).returning(User.id)

                result = await session.execute(smtm)
                inserted_id = result.scalar_one_or_none()
                await session.commit()

                if inserted_id is not None:
                    query = select(User).options(
                        joinedload(User.role)
                    ).where(User.id == inserted_id)

                    result = await session.execute(query)

                    user = result.unique().scalar_one_or_none()

                    encoded = jsonable_encoder(user)

                    return UserOutput(**encoded)

                return None
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def delete_all(self):
        """
        Implementation to delete all data in database, used for tests only.
        :return:
        """

        try:
            session = async_sessionmaker(self.pg_engine, autoflush=False)
            async with session() as session:
                smtm = delete(User)
                await session.execute(smtm)
                await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def delete_by_id(self, user_id: str):
        try:
            session = async_sessionmaker(self.pg_engine)
            async with session() as session:
                smtm = delete(User).where(User.id == user_id).returning(
                    User.id
                )
                result = await session.execute(smtm)
                user_id_deleted = result.scalar_one_or_none()
                await session.commit()
                return user_id_deleted
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def find_by_id(self, user_id: str):
        session = async_sessionmaker(self.pg_engine)
        async with session() as session:
            smtm = select(User).where(User.id == user_id)
            result = await session.execute(smtm)
            permission = result.scalar_one_or_none()
            if permission is not None:
                return UserOutput(**permission.__dict__)
            return None

