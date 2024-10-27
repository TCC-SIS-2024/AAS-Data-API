from typing import List, Any
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, ConfigDict

class Pagination(BaseModel):
    """
    Pagination model representing the pagination in the application.
    """
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=10)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            int: lambda v: int(v)
        },
    )

class PaginationResponse(BaseModel):
    """
    Pagination response model representing the pagination response in the application.
    """
    data: List[Any]
    total: int

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            uuid: lambda v: str(v)
        },
    )