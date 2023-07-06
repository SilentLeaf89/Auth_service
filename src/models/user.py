from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from .base import Base, DatabaseBaseModel


user_role_table = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)


class User(DatabaseBaseModel, Base):
    __tablename__ = "user"

    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))

    roles = relationship(
        "Role", secondary=user_role_table, back_populates="users"
    )

    def __repr__(self) -> str:
        return f"<User {self.login}>"
