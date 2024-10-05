from src.domain.entities.user import UserInput, UserOutput
from src.domain.interfaces.repositories import IUserRepository
from uuid import uuid4
from datetime import datetime, timezone

class UserRepositoryMock(IUserRepository):
    async def find_by_email(self, email: str) -> UserOutput | None:
        user = {
            "id": uuid4(),
            "username": "teste",
            "email": "teste@email.com",
            "password": "teste123",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        return UserOutput(**user)

    async def create(self, user_input: UserInput) -> UserOutput | None:
        pass