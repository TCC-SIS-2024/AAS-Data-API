from datetime import datetime, timezone
from asyncua.ua.uaprotocol_auto import ReadRawModifiedDetails

from src.domain.entities.history import HistoryDataAAS
from src.domain.interfaces.repositories import IAASHistoryData
from asyncua import Client
import os
import json
from motor.motor_asyncio import AsyncIOMotorClient


class AASHistoryRepository(IAASHistoryData):

    async def get_history_data_from_aas(self, start_time: datetime, end_time: datetime, opcua_server_host: str, opcua_server_port: int):

        async with Client(f"opc.tcp://{opcua_server_host}:{opcua_server_port}") as opcua_client:
            endpoint_info_as_json = await opcua_client.nodes.server.call_method("0:GetEndpointHistoryData")
            endpoint_info_dict = json.loads(endpoint_info_as_json)

            connection_params = {
                "host": '0.0.0.0',
                "port": endpoint_info_dict['database_port'],
                "user": endpoint_info_dict['database_user'],
                "password": endpoint_info_dict['database_password']
            }

            motor_asyncio_client = AsyncIOMotorClient(
                host=connection_params['host'],
                port=connection_params['port'],
                username=connection_params['user'],
                password=connection_params['password']
            )

            aas_database = motor_asyncio_client.get_database('asset-adminstration-shell')
            variable_history_coll = aas_database.get_collection('variable_history')

            pipeline = [
                {
                    "$match": {
                        '$and': [
                            {'timestamp': {'$gte': start_time}},
                            {'timestamp': {'$lte': end_time}},
                            {'idShort': {'$in': ['Temperature', 'Humidity']}}
                        ]
                    }
                }
            ]

            cursor = variable_history_coll.aggregate(pipeline)
            cursor = cursor.batch_size(1000)


            temp_humidity_batch = []
            all_results = []

            async for document in cursor:
                temp_humidity_batch.append(json.loads(HistoryDataAAS(**document).model_dump_json()))
                if len(temp_humidity_batch) == 1000:
                    await self._process_batch(temp_humidity_batch, all_results)
                    temp_humidity_batch = []

            if temp_humidity_batch:
                await self._process_batch(temp_humidity_batch, all_results)

            return all_results, len(all_results)
    @staticmethod
    async def _process_batch(batch, all_results):
        all_results.extend(batch)