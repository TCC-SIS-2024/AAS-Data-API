from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class ValueDocument(BaseModel):
    value: float
    data_type: int
    source_timestamp: datetime
    server_timestamp: datetime

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
        }
    )



class HistoryDataAAS(BaseModel):
    id: ObjectId = Field(alias="_id")
    idShort: str
    category: str
    value: ValueDocument
    valueType: str
    timestamp: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            ObjectId: lambda v: str(v),
        },
    )



