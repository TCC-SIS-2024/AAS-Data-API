from typing import Optional, Any, List
from src.domain.entities.role import RoleInput, RoleOutput
from src.domain.interfaces.repositories import IRoleRepository
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import joinedload
from src.infra.databases.pgdatabase import Role, Permission, role_permission_association
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, or_, delete, update

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
                smtm = insert(Role).values(name=role_input.name).returning(Role.id)
                result = await session.execute(smtm)
                inserted_id = result.scalar_one_or_none()

                if inserted_id is not None and role_input.permission_ids is not None:

                    permission_smtm = insert(role_permission_association).values(
                        [{"role_id": inserted_id, "permission_id": permission_id} for permission_id in role_input.permission_ids]
                    )

                    await session.execute(permission_smtm)

                    await session.commit()

                    query = select(Role).options(
                        joinedload(Role.permissions),
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

    async def find_all(self, page: int = 1, page_size: int = 10, search_input: Optional[Any] = None):
        """
        Implementation of abstract method `find_all` which will find all roles
        :return:  fetched in database
        """

        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            offset = (page - 1) * page_size

            smtm = select(Role).options(
                joinedload(Role.permissions)
            ).limit(page_size).offset(offset)

            search_conditions = []

            if search_input is not None:
                if isinstance(search_input, str):
                    search_conditions.append(Role.name.ilike(f"%{search_input}%"))

            if search_conditions:
                smtm = smtm.where(or_(*search_conditions))

            result = await session.execute(smtm)
            fetched_roles = result.unique().scalars()
            roles: List[RoleOutput] = []

            for user in fetched_roles.fetchall():
                encoded = jsonable_encoder(user)
                roles.append(RoleOutput(**encoded))

            return roles

        return None

    async def find_by_id(self, role_id: str):
        session = async_sessionmaker(self.pg_engine)
        async with session() as session:
            smtm = select(Role).options(joinedload(Role.permissions)).where(Role.id == role_id)
            result = await session.execute(smtm)
            role = result.unique().scalar_one_or_none()
            encoded = jsonable_encoder(role)
            if role is not None:
                return RoleOutput(**encoded)
            return None

    async def delete_by_id(self, role_id: str):
        try:
            session = async_sessionmaker(self.pg_engine)
            async with session() as session:
                smtm = delete(Role).where(Role.id == role_id).returning(
                    Role.id
                )
                result = await session.execute(smtm)
                deleted_id_deleted = result.scalar_one_or_none()
                await session.commit()
                return deleted_id_deleted
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def count_roles(self):
        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            smtm = select(Role)
            result = await session.execute(smtm)
            roles_qtd = len(result.scalars().fetchall())
            return roles_qtd

        return None

    async def update_by_id(self, role: RoleInput, role_id: str):
        try:
            session = async_sessionmaker(self.pg_engine, autoflush=False)
            async with session() as session:
                smtm = update(Role).values(
                    name=role.name,
                    permission_id=role.permission_id or None
                ).where(Role.id == role_id).returning(Role)

                result = await session.execute(smtm)
                role = result.scalar_one_or_none()
                updated_role = RoleOutput(**role.__dict__)
                await session.commit()

                if role is not None:
                    return updated_role
        except:
            await session.rollback()
            raise
        finally:
            await session.close()