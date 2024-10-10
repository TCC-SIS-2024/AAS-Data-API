import pytest
import httpx
from server import app
import pytest_asyncio

from src.adapters.repositories.user_repository import UserRepository
from src.application.usecases.sign_in import SignInUseCase
from src.domain.entities.user import UserInput
from src.web.dependencies import pg_engine, jwt_encoder
from fastapi.security import OAuth2PasswordRequestForm


@pytest_asyncio.fixture(loop_scope="package")
async def setup_fake_user():
    engine = pg_engine()
    encoder = jwt_encoder()
    repository = UserRepository(engine)
    await repository.delete_all()
    password = encoder.get_password_hash('mock123')
    await repository.create(
        UserInput(username='mock_user', email='mock@email.com', password=password)
    )

    sign_in = SignInUseCase(repository)

    form = {
        "username": "mock@email.com",
        "password": 'mock123'
    }

    response = await sign_in.execute(OAuth2PasswordRequestForm(**form))
    token = response.payload['access_token']
    yield token

@pytest.mark.asyncio(loop_scope="package")
async def test_system_status(setup_fake_user):
    token = setup_fake_user
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        response = await client.get("api/v1/system/status/", headers={
            "Authorization": f"Bearer {token}"
        })

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