import pytest
import httpx
from server import app
import pytest_asyncio
from src.adapters.repositories.user_repository import UserRepository
from src.domain.entities.user import UserInput
from src.web.dependencies import pg_engine, jwt_encoder

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

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_200(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": "mock@email.com",
            "password": "mock123"
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 200

    response_json = response.json()
    assert 'access_token' in response_json
    assert 'token_type' in response_json

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_404(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": "mock_other@email.com",
            "password": "mock123"
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 404
    response_json = response.json()
    assert response_json['payload'] == 'User not found!'

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_401(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": "mock@email.com",
            "password": "mock1232"
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 401
    response_json = response.json()
    assert response_json['payload'] == 'Invalid credentials'

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_422(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": "mock",
            "password": "mock1232"
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_422_with_no_email(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": "mock",
            "password": None
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_422_with_no_pass(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": None,
            "password": "234234"
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_422_with_empty_email(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": "",
            "password": "234234"
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 422

@pytest.mark.asyncio(loop_scope="package")
async def test_ensure_sign_in_returns_422_with_empty_password(setup_fake_user):
    http_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )
    async with http_client as client:
        form = {
            "username": "teste@email.com",
            "password": ""
        }

        response = await client.post("api/v1/auth/sign-in/", data=form)

    assert response.status_code == 422