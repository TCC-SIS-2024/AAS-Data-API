import pytest
import httpx
from server import app
from src.adapters.repositories.user_repository import UserRepository
from src.application.usecases.sign_in import SignInUseCase
from src.domain.entities.user import UserInput
from src.web.dependencies import pg_engine, jwt_encoder
import pytest_asyncio
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
async def test_ensure_creation_role_returns_200(setup_fake_user):
    token = setup_fake_user
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:

        role_content = {
            "name": "admin",
            "users": [],
            "permissions": []
        }

        response = await client.post("api/v1/roles/", headers={
            'Authorization': f'Bearer {token}'
        }, json=role_content)

        assert response.status_code == 200
        response_json = response.json()

        assert 'status_code' in response_json
        assert 'payload' in response_json

        payload = response_json['payload']

        assert 'id' in payload
        assert 'name' in payload
        assert 'created_at' in payload
        assert 'updated_at' in payload
        assert 'users' in payload
        assert 'permissions' in payload