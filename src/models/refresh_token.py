import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base, DatabaseBaseModel


class RefreshToken(DatabaseBaseModel, Base):
    __tablename__ = "refresh_token"

    token = Column(String(1000))
    user_id = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
