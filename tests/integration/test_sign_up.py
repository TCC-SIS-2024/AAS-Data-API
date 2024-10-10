from datetime import datetime
from uuid import UUID

import pytest
import httpx
from server import app
import pytest_asyncio
from src.adapters.repositories.user_repository import UserRepository
from src.web.dependencies import pg_engine

@pytest_asyncio.fixture(loop_scope="package")
async def setup_fake_user():
    engine = pg_engine()
    repository = UserRepository(engine)
    await repository.delete_all()

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_up_returns_200(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        payload = {
            "username": "mock_user",
            "email": "mock@email.com",
            "password": "mock123",
        }

        response = await client.post("api/v1/auth/sign-up/", json=payload)

    assert response.status_code == 200
    response_json = response.json()

    assert 'status_code' in response_json
    assert 'payload' in response_json
    assert response_json['status_code'] == 200

    response_body = response.json()['payload']

    assert 'id' in response_body
    assert 'username' in response_body
    assert 'password' in response_body
    assert 'created_at' in response_body
    assert 'updated_at' in response_body
    assert 'email' in response_body

    assert isinstance(UUID(response_body['id']), UUID)
    assert isinstance(datetime.fromisoformat(response_body['created_at']), datetime)
    assert isinstance(datetime.fromisoformat(response_body['updated_at']), datetime)


@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_up_returns_422(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        payload = {
            "username": "",
            "email": "mock@email.com",
            "password": "mock123",
        }

        response = await client.post("api/v1/auth/sign-up/", json=payload)

    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_up_returns_422_no_email(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        payload = {
            "username": "mock_user",
            "email": "",
            "password": "mock123",
        }

        response = await client.post("api/v1/auth/sign-up/", json=payload)

    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_up_returns_422_no_password(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        payload = {
            "username": "mock_user",
            "email": "email@email.com",
            "password": "",
        }

        response = await client.post("api/v1/auth/sign-up/", json=payload)

    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_up_returns_422_no_fields(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        payload = {}

        response = await client.post("api/v1/auth/sign-up/", json=payload)

    assert response.status_code == 422
