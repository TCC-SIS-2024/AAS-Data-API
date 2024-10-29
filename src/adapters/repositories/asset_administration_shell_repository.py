from typing import List, Optional, Any
from uuid import UUID
from src.domain.entities.asset_administration_shell import AssetAdministrationShellInput, AssetAdministrationShellOutput
from src.domain.interfaces.repositories import IAssetAdministrationShellRepository
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy import insert, select, String, or_, Integer, delete
from src.infra.databases.pgdatabase import AssetAdministrationShell


class AssetAdministrationShellRepository(IAssetAdministrationShellRepository):

    def __init__(self, pg_engine: AsyncEngine):
        self.pg_engine: AsyncEngine = pg_engine

    async def delete_by_id(self, aas_id: str):
        try:
            session = async_sessionmaker(self.pg_engine)
            async with session() as session:
                smtm = delete(AssetAdministrationShell).where(AssetAdministrationShell.id == aas_id).returning(
                    AssetAdministrationShell.id
                )
                result = await session.execute(smtm)
                aas_id_deleted = result.scalar_one_or_none()
                await session.commit()
                return aas_id_deleted
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def count_all_asset_administration_shells(self):
        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            smtm = select(AssetAdministrationShell)
            result = await session.execute(smtm)
            aas_qtd = len(result.scalars().fetchall())
            return aas_qtd

        return None
    @staticmethod
    def parse_search_input(search_input: str):
        try:
            return int(search_input)
        except ValueError:
            pass

        try:
            return float(search_input)
        except ValueError:
            pass

        try:
            return bool(search_input)
        except ValueError:
            pass

        return search_input

    async def find_all(self, page: int = 1, page_size: int = 10, search_input: Optional[Any] = None):
        session = async_sessionmaker(self.pg_engine)

        async with session() as session:
            offset = (page - 1) * page_size

            smtm = select(AssetAdministrationShell).limit(page_size).offset(offset)

            search_conditions = []

            if search_input is not None:
                if isinstance(search_input, str):
                    search_conditions.append(AssetAdministrationShell.id_short.ilike(f"%{search_input}%"))
                    search_conditions.append(AssetAdministrationShell.database_endpoint.ilike(f"%{search_input}%"))
                    search_conditions.append(AssetAdministrationShell.host.ilike(f"%{search_input}%"))

            if search_conditions:
                smtm = smtm.where(or_(*search_conditions))

            result = await session.execute(smtm)
            fetched_aas = result.scalars()
            asset_administration_shells: List[AssetAdministrationShellOutput] = []

            for aas in fetched_aas.fetchall():
                asset_administration_shells.append(AssetAdministrationShellOutput(**aas.__dict__))

            return asset_administration_shells

        return None

    async def find_by_id_short(self, id_short: str):
        pass

    async def find_by_host(self, host: str):
        pass

    async def create(self, aas: AssetAdministrationShellInput):
        try:
            session = async_sessionmaker(self.pg_engine, autoflush=False)
            async with session() as session:
                smtm = insert(AssetAdministrationShell).values(
                    id_short=aas.id_short,
                    database_endpoint=aas.database_endpoint,
                    host=aas.host,
                    aas_modeling=aas.aas_modeling,
                    active=aas.active,
                    port=aas.port,
                ).returning(AssetAdministrationShell)

                result = await session.execute(smtm)
                aas = result.scalar_one_or_none()
                inserted_aas = AssetAdministrationShellOutput(**aas.__dict__)
                await session.commit()

                if aas is not None:
                    return inserted_aas
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def update(self, aas: AssetAdministrationShellInput):
        pass

    async def delete(self, id_short: str):
        pass