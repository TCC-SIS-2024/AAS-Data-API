import os
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Uuid, func, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from typing import List

url = URL.create(
    drivername="postgresql+asyncpg",
    username=os.environ.get('POSTGRES_USER', None),
    password=os.environ.get('POSTGRES_PASSWORD', None),
    host=os.environ.get('POSTGRES_HOST', None),
    port=int(os.environ.get('POSTGRES_PORT', None)),
    database=os.environ.get('POSTGRES_DB', None),
)

engine: AsyncEngine = create_async_engine(url)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = MappedColumn(Uuid(), default=uuid.uuid4, unique=True, nullable=False, primary_key=True)
    username: Mapped[str] = MappedColumn(String(255), unique=True)
    email: Mapped[str] = MappedColumn(String(255), unique=True)
    password: Mapped[str] = MappedColumn(String(255), unique=True)
    role_id: Mapped[str] = MappedColumn(ForeignKey("roles.id"), nullable=True)
    role: Mapped['Role'] = relationship('Role', back_populates='users')
    created_at: Mapped[datetime] = MappedColumn(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = MappedColumn(DateTime(timezone=True), default=func.now(), onupdate=func.now(),
                                                nullable=False)

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[str] = MappedColumn(Uuid(), default=uuid.uuid4, unique=True, nullable=False, primary_key=True)
    name: Mapped[str] = MappedColumn(String(255), unique=True)
    permission_id: Mapped[str] = MappedColumn(ForeignKey("roles.id"), nullable=True)
    permission: Mapped['Permission'] = relationship('Permission', back_populates='roles')
    created_at: Mapped[datetime] = MappedColumn(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = MappedColumn(DateTime(timezone=True), default=func.now(), onupdate=func.now(),
                                                nullable=False)
    users: Mapped[List[User]] = relationship('User', back_populates='role')

class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[str] = MappedColumn(Uuid(), default=uuid.uuid4, unique=True, nullable=False, primary_key=True)
    value: Mapped[str] = MappedColumn(String(255), unique=True)
    created_at: Mapped[datetime] = MappedColumn(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = MappedColumn(DateTime(timezone=True), default=func.now(), onupdate=func.now(),
                                                nullable=False)

    roles: Mapped[List[Role]] = relationship('Role', back_populates='permission')