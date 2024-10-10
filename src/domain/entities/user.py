import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.fields import Field
from pydantic.networks import EmailStr


class UserInput(BaseModel):
    """
    User model representing a user in the application with additional fields for input.
    """
    username: str = Field(max_length=100, min_length=5)
    email: EmailStr
    password: str = Field(max_length=100, min_length=6)

class UserOutput(UserInput):
    """
    User model representing a user in the application with additional fields for output.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            uuid: lambda v: str(v)
        },
    )