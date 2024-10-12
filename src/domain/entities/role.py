from datetime import datetime
from uuid import UUID
import uuid
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from src.domain.entities.permission import PermissionOutput


class RoleInput(BaseModel):
    """
    Role model representing a role in the application with additional fields for input.
    """
    name: str = Field(max_length=50, min_length=3)
    permission_id: Optional[UUID] = None


class RoleOutput(RoleInput):
    """
    Role model representing a user in the application with additional fields for output.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    permission: Optional[PermissionOutput] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            uuid: lambda v: str(v)
        },
    )
