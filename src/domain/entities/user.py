import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    """
    User model representing a user in the application.
    """
    username: str
    email: str

class UserOutput(UserBase):
    """
    User model representing a user in the application with additional fields for output.
    """
    id: uuid
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            uuid: lambda v: str(v)
        },
    )

class UserInput(UserBase):
    """
    User model representing a user in the application with additional fields for input.
    """
    pass
