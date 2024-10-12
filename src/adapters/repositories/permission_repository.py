from src.domain.entities.permission import PermissionInput, PermissionOutput
from src.domain.interfaces.repositories import IPermissionRepository
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy import insert
from src.infra.databases.pgdatabase import Permission


class PermissionRepository(IPermissionRepository):

    def __init__(self, pg_engine: AsyncEngine):
        self.pg_engine: AsyncEngine = pg_engine

    async def create(self, permission_input: PermissionInput) -> PermissionOutput:
        """
        This abstract method is responsible for storing the role on the database and return it information.
        :param permission_input:
        :return: role information
        """

        try:
            session = async_sessionmaker(self.pg_engine, autoflush=False)
            async with session() as session:
                smtm = insert(Permission).values(
                    value=permission_input.value,
                ).returning(Permission)

                result = await session.execute(smtm)
                permission = result.scalar_one_or_none()
                inserted_permission = PermissionOutput(**permission.__dict__)
                await session.commit()


                if permission is not None:
                    return inserted_permission

                return None
        except:
            await session.rollback()
            raise
        finally:
            await session.close()