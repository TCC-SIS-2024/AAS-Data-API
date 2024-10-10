from pydantic import BaseModel
from typing import List

class Database(BaseModel):
    version: str
    name: str
    max_connections: int
    opened_connections: int

class PostgreSQL(Database):
    name: str = 'postgres'

class Dependencies(BaseModel):
    databases: List[Database]


class SystemStatus(BaseModel):
    dependencies: Dependencies