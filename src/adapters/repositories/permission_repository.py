from typing import Optional, Any, List

from src.domain.entities.permission import PermissionInput, PermissionOutput
from src.domain.interfaces.repositories import IPermissionRepository
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy import insert, select, or_, delete
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

    async def find_all(self, page: int = 1, page_size: int = 10, search_input: Optional[Any] = None):
        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            offset = (page - 1) * page_size

            smtm = select(Permission).limit(page_size).offset(offset)

            search_conditions = []

            if search_input is not None:
                if isinstance(search_input, str):
                    search_conditions.append(Permission.value.ilike(f"%{search_input}%"))

            if search_conditions:
                smtm = smtm.where(or_(*search_conditions))

            result = await session.execute(smtm)
            fetched_permissions = result.scalars()
            permissions: List[PermissionOutput] = []

            for permission in fetched_permissions.fetchall():
                permissions.append(PermissionOutput(**permission.__dict__))

            return permissions

        return None

    async def find_by_id(self, permission_id: str):
        session = async_sessionmaker(self.pg_engine)
        async with session() as session:
            smtm = select(Permission).where(Permission.id == permission_id)
            result = await session.execute(smtm)
            permission = result.scalar_one_or_none()
            if permission is not None:
                return PermissionOutput(**permission.__dict__)
            return None

    async def update_by_id(self, permission: PermissionInput, permission_id: str):
        pass

    async def delete_by_id(self, permission_id: str):
        try:
            session = async_sessionmaker(self.pg_engine)
            async with session() as session:
                smtm = delete(Permission).where(Permission.id == permission_id).returning(
                    Permission.id
                )
                result = await session.execute(smtm)
                permission_id_deleted = result.scalar_one_or_none()
                await session.commit()
                return permission_id_deleted
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def count_permissions(self):
        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            smtm = select(Permission)
            result = await session.execute(smtm)
            permissions_qtd = len(result.scalars().fetchall())
            return permissions_qtd