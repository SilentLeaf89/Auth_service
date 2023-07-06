from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base, DatabaseBaseModel


class UserHistory(DatabaseBaseModel, Base):
    __tablename__ = "user_history"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    event = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<UserHistory {self.event}>"
