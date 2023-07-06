from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field, validator

from schemas.base import Base


class RoleModel(Base):
    name: str = Field(max_length=255)
    access: str = Field(max_length=255)

    class Config:
        orm_mode = True


class RoleUpdateModel(RoleModel):
    name: str | None = Field(max_length=255)


class RoleResponseModel(RoleModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime

class RoleDeleteMessage(Base):
    msg : str
