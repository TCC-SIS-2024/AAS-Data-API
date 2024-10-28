from datetime import datetime
from uuid import UUID
import uuid
from pydantic import BaseModel, Field, ConfigDict


class AssetAdministrationShellInput(BaseModel):
    """
    AssetAdministrationShell model representing a role in the application with additional fields for input.
    """
    id_short: str = Field(max_length=50, min_length=3)
    database_endpoint: str = Field(max_length=50, min_length=3)
    aas_modeling: str = Field(max_length=50, min_length=3)
    host: str = Field(max_length=50, min_length=3)
    active: bool = Field(default=False)
    port: int = Field(default=4041)


class AssetAdministrationShellOutput(AssetAdministrationShellInput):
    """
    AssetAdministrationShell model representing a user in the application with additional fields for output.
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
