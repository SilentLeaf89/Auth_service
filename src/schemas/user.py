from uuid import UUID
from datetime import datetime

from pydantic import Field

from schemas.base import Base
from schemas.role import RoleModel


class UserCreate(Base):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(max_length=255)
    first_name: str | None
    last_name: str | None


class UserInDB(Base):
    id: UUID
    first_name: str | None
    last_name: str | None


class UserHistoryAdd(Base):
    user_id: UUID
    event: str = Field(max_length=255)

    class Config:
        orm_mode = True


class UserHistoryShow(Base):
    event: str = Field(max_length=255)
    created_at: datetime

    class Config:
        orm_mode = True


class UserRoleAction(Base):
    user_id: UUID
    role_id: UUID


class UserSchema(UserInDB):
    login: str

    class Config:
        orm_mode = True
