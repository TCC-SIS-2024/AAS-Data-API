from unittest.async_case import IsolatedAsyncioTestCase
from server import app
import httpx
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.adapters.libs.bcrypt import BcryptAdapter
from src.web.dependencies import pg_engine
from src.infra.databases.pgdatabase import User


class AuthenticationTestCase(IsolatedAsyncioTestCase):

    def get_client(self):
        return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver")

    def setUp(self):
        self.encoder = BcryptAdapter()

    async def asyncSetUp(self):
        """
        Set up resources before each test. This includes inserting mock user data.
        """
        password = self.encoder.get_password_hash('mock_password')
        engine = pg_engine()
        session = async_sessionmaker(engine)
        async with session() as session:
            # Delete existing users
            await session.execute(delete(User))

            # Insert mock user
            stmt = insert(User).values(
                username="mock_user",
                email="mock@email.com",
                password=password,
            )
            await session.execute(stmt)
            await session.commit()


    async def test_authentication_use_cases(self):

        data = {
            "username": 'mock@email.com',
            "password": 'mock_password'
        }

        client = self.get_client()
        async with client as client:
            response = await client.post('/auth/sign-in/', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json())
            self.assertIn('token_type', response.json())
            self.assertEqual('bearer', response.json()['token_type'])

        data = {
            "username": 'other@email.com',
            "password": 'other'
        }

        client = self.get_client()
        async with client as client:
            response = await client.post('/auth/sign-in/', data=data)
            self.assertEqual(response.status_code, 404)

        data = {
            "username": '',
            "password": ''
        }

        client = self.get_client()
        async with client as client:
            response = await client.post('/auth/sign-in/', data=data)
            self.assertEqual(response.status_code, 422)

        data = {
            "username": 'lucas@email.com',
        }

        client = self.get_client()
        async with client as client:
            response = await client.post('/auth/sign-in/', data=data)
            self.assertEqual(response.status_code, 422)

        data = {
            "username": 123123,
            "password": 1231
        }

        client = self.get_client()
        async with client as client:
            response = await client.post('/auth/sign-in/', data=data)
            self.assertEqual(response.status_code, 422)

        data = {
            "username": "mock@email.com",
            "password": "DROP DATABASE users"
        }

        client = self.get_client()
        async with client as client:
            response = await client.post('/auth/sign-in/', data=data)
            self.assertEqual(response.status_code, 401)

        data = {
            "username": "mock@email.com",
            "password": "oi7gl"
        }

        client = self.get_client()
        async with client as client:
            response = await client.post('/auth/sign-in/', data=data)
            self.assertEqual(response.status_code, 401)




    def tearDown(self):
        self.client = None