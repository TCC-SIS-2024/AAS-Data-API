from unittest.async_case import IsolatedAsyncioTestCase
from server import app
import httpx


class AuthenticationTestCase(IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver")

    async def test_sign_in_should_return_200(self):

        payload_form_data = {
            'username': 'teste',
            'password': 'teste'
        }

        async with self.client as client:
            response = await client.post('/auth/sign-in/', data=payload_form_data)

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client = None