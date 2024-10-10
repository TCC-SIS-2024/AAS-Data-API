import os

from src.domain.interfaces.repositories import ISystemRepository
from sqlalchemy import select, column, text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

class SystemRepository(ISystemRepository):
    """ Class implementation for IUserRepository with all methods """

    def __init__(self, pg_engine: AsyncEngine):
        self.pg_engine: AsyncEngine = pg_engine

    async def postgres_database_version(self):
        """
        Implementation of abstract method `postgres_database_version` which will return the version of the PostgreSQL database.
        :return: version of current postgres database
        """

        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            smtm = text("SHOW server_version;")

            result = await session.execute(smtm)

            version = result.scalar_one_or_none()

            return version or None

    async def postgres_max_connections(self):
        """
        Implementation of abstract method `postgres_max_connections` which will return the max connections of the PostgreSQL database.
        :return: max connections of the PostgreSQL database
        """

        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            smtm = text("SHOW max_connections;")

            result = await session.execute(smtm)

            max_connections = result.scalar_one_or_none()

            return max_connections or None

    async def postgres_opened_connections(self):
        """
        Implementation of abstract method `postgres_opened_connections` which will return the opened connections of the PostgreSQL database.
        :return: opened connections of the PostgreSQL database
        """

        session = async_sessionmaker(self.pg_engine)
        database_name: str = os.environ.get('POSTGRES_DB')

        async with session() as session:
            smtm = text("SELECT count(*)::int FROM pg_stat_activity WHERE datname = :database_name;")

            result = await session.execute(smtm, {
                'database_name': database_name
            })

            opened_connections = result.scalar_one_or_none()

            return opened_connections or None