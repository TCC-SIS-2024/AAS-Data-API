import pytest
import httpx
from server import app

@pytest.mark.asyncio(loop_scope="package")
async def test_system_status():
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        response = await client.get("api/v1/system/status/")

        assert response.status_code == 200
        response_json = response.json()

        version = response_json['payload']['dependencies']['databases'][0]['version']
        name = response_json['payload']['dependencies']['databases'][0]['name']
        max_connections = response_json['payload']['dependencies']['databases'][0]['max_connections']
        opened_connections = response_json['payload']['dependencies']['databases'][0]['opened_connections']
        assert version == '16.4'
        assert name == 'postgres'
        assert max_connections == 100
        assert opened_connections is not None