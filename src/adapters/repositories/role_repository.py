from src.domain.entities.permission import PermissionOutput
from src.domain.entities.role import RoleInput, RoleOutput
from src.domain.interfaces.repositories import IRoleRepository
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload
from src.infra.databases.pgdatabase import Role, Permission
from fastapi.encoders import jsonable_encoder

class RoleRepository(IRoleRepository):

    def __init__(self, pg_engine: AsyncEngine):
        self.pg_engine: AsyncEngine = pg_engine

    async def create(self, role_input: RoleInput) -> RoleOutput | None:
        """
        This abstract method is responsible for storing the role on the database and return it information.
        :param role_input:
        :return: role information
        """

        try:
            session = async_sessionmaker(self.pg_engine, autoflush=False)
            async with session() as session:
                smtm = insert(Role).values(
                    name=role_input.name,
                    permission_id=role_input.permission_id or None
                ).returning(Role.id)

                result = await session.execute(smtm)
                inserted_id = result.scalar_one_or_none()
                await session.commit()

                if inserted_id is not None:
                    query = select(Role).options(
                        joinedload(Role.permission),
                        joinedload(Role.users)
                    ).where(Role.id == inserted_id)

                    result = await session.execute(query)

                    role = result.unique().scalar_one_or_none()

                    encoded = jsonable_encoder(role)

                    return RoleOutput(**encoded)

                return None
        except:
            await session.rollback()
            raise
        finally:
            await session.close()