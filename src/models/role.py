from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base, DatabaseBaseModel
from .user import user_role_table


class Role(DatabaseBaseModel, Base):
    __tablename__ = "role"

    name = Column(String(255), unique=True, nullable=False)
    access = Column(String(255), nullable=False)

    users = relationship(
        "User", secondary=user_role_table, back_populates="roles"
    )

    def __repr__(self) -> str:
        return f"<Role {self.name}>"
