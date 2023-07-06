from uuid import UUID

from sqlalchemy import insert, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from models.user import User, user_role_table
from models.role import Role
from repositories.postgres_db import PostgresDB

from utils.exceptions import UserRoleActionError


class UserDB(PostgresDB):
    table = User

    async def add_role_to_user(self, user_id: UUID, role_id: UUID) -> None:
        """Add role to user
        use directly database connection to add many-to-many link

        Args:
            user_id (UUID): id of the user
            role_id (UUID): id of the role

        Raises:
            UserRoleActionError: if role already added
        """
        async with self.connection.connect() as conn:
            statement = insert(user_role_table).values(
                user_id=user_id, role_id=role_id
            )
            try:
                result = await conn.execute(statement)
            except IntegrityError:
                raise UserRoleActionError("Role already added")

            # if query finish success
            if result.rowcount > 0:
                await conn.commit()
            else:
                await conn.rollback()
                raise UserRoleActionError

    async def delete_role_from_user(
        self, user_id: UUID, role_id: UUID
    ) -> None:
        async with self.connection.connect() as conn:
            statement = user_role_table.delete().where(
                and_(
                    user_role_table.c.user_id == user_id,
                    user_role_table.c.role_id == role_id,
                )
            )
            try:
                result = await conn.execute(statement)
            except IntegrityError:
                raise UserRoleActionError("Failed to remove role")

            if result.rowcount > 0:
                await conn.commit()
            else:
                await conn.rollback()
                raise UserRoleActionError

    async def get_user_roles(self, user_id: UUID) -> list[dict]:
        """get all roles assigned to the user

        Args:
            user_id (UUID): id of the user

        Returns:
            list[dict]: dict of roles prepared to be load in pydantic model
        """
        async with self.connection.connect() as conn:
            statement = (
                select(Role.id, Role.name, Role.access, Role.created_at)
                .join(Role.users)
                .filter(User.id == user_id)
            )
            result = await conn.execute(statement)
            rows = result.fetchall()

            roles = [
                {
                    "id": str(role_id),
                    "name": role_name,
                    "access": role_access,
                    "created_at": role_created_at,
                }
                for role_id, role_name, role_access, role_created_at in rows
            ]
        return roles
