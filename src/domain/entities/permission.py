from datetime import datetime
from uuid import UUID
import uuid
import re
from pydantic import BaseModel, Field, ConfigDict, field_validator

class PermissionInput(BaseModel):
    """
    Permission model representing a role in the application with additional fields for input.
    """
    value: str = Field(default="create:read:update:delete")

    @field_validator('value', mode='before')
    @classmethod
    def validate_format(cls, value: str) -> str:
        matched = re.match("^([a-zA-Z]+)(:[a-zA-Z]+)*$", value)
        if matched:
            print(value)
            return value
        else:
            raise ValueError("Invalid permission format. It should be like 'create:read:update:delete'")

class PermissionOutput(PermissionInput):
    """
    Permission model representing a permission in the application with additional fields for output.
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
        extra='ignore'
    )