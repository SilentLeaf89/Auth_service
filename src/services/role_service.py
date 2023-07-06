from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine

from db.postgres import get_postgres
from core.get_logger import logger
from repositories.abstract_db import AbstractDB
from repositories.role_db import RoleDB
from repositories.user_db import UserDB
from utils.exceptions import (
    UserRoleActionError,
    NotFoundError,
    RoleNotAssigned,
    AlreadyExistError,
)
from schemas.role import RoleModel, RoleResponseModel, RoleUpdateModel, RoleDeleteMessage
from schemas.user import UserRoleAction


class RoleService:
    def __init__(
        self,
        role_repository: RoleDB,
        user_repository: UserDB,
    ) -> None:
        self.role_repository = role_repository
        self.user_repository = user_repository

    async def get(self, id: UUID) -> RoleResponseModel:
        logger.debug("[RoleService][get] - trying to get role by id %s", id)
        result = await self.role_repository.get(id)
        if not result:
            logger.debug("[RoleService][get] - role %s not found", id)
            raise NotFoundError("Role {} not found.".format(id))
        logger.info("[RoleService][get] - role found")
        return RoleResponseModel.from_orm(result[0])

    async def get_all(self) -> list[RoleResponseModel]:
        query_result = await self.role_repository.get_all()
        logger.debug("[RoleService][get_all] - Trying to get all roles")
        result = [RoleResponseModel.from_orm(item) for item in query_result]
        if not result:
            logger.debug("[RoleService][get_all] - roles not found")
            raise NotFoundError("No roles")
        logger.info("[RoleService][get_all] - %s roles found", len(result))
        return result

    async def find(self, name: str) -> RoleResponseModel | None:
        """find role by name
        used when need to find role without any axception.
        for example when role add
        Args:
            name (str): name of the role

        Returns:
            RoleResponseModel | None: role entity or None
        """
        logger.debug(
            "[RoleService][find] - trying to find role by name %s", name
        )
        result = await self.role_repository.find({"name": name})

        if not result:
            logger.debug("[RoleService][find] - role %s not found", name)
            return None

        logger.info("[RoleService][find] - role found")
        return RoleResponseModel.from_orm(result[0])

    async def add(self, new_role: RoleModel) -> RoleResponseModel:
        logger.debug(
            "[RoleService][add] - trying to add role %s", new_role.name
        )

        result = await self.find(new_role.name)

        if result:
            logger.debug(
                "[RoleService][add] - role %s already exist", new_role.name
            )
            raise AlreadyExistError(
                "Role {} already exist.".format(new_role.name)
            )

        result = await self.role_repository.insert(new_role)

        result = result[0]

        logger.info("[RoleService][add] - new role added")
        return RoleResponseModel.from_orm(result)

    async def update(
        self, id: UUID, updated_role: RoleUpdateModel
    ) -> RoleResponseModel:
        await self.get(id)
        logger.debug(
            "[RoleService][update] - trying to update role %s",
            updated_role.name,
        )
        query_result = await self.role_repository.update(id, updated_role)
        logger.info("[RoleService][update] - role updated")
        return RoleResponseModel.from_orm(query_result[0])

    async def delete(self, id: UUID) -> RoleDeleteMessage:
        await self.get(id)
        logger.debug(
            "[RoleService][delete] - trying to delete role id %s",
            id,
        )
        await self.role_repository.delete(id)

        logger.info("[RoleService][delete] - role deleted")
        return RoleDeleteMessage(msg="Role {} deleted successfully".format(id))

    async def _check_entity_exist(
        self, entity_id: UUID, repository: AbstractDB
    ) -> None:
        """check abstract entity exist in abstract repository

        Args:
            entity_id (UUID): entity id (user or role)
            repository (AbstractDB): repository (user or role)

        Raises:
            NotFoundError: if not entity found
        """
        logger.debug(
            "[RoleService][_check_entity_exist] - "
            "check entity %s in repository %s",
            entity_id,
            repository.table,
        )
        entity = await repository.get(entity_id)
        if not entity:
            logger.debug(
                "[RoleService][_check_entity_exist] - "
                "entity %s not found in repository %s",
                entity_id,
                repository.table,
            )
            raise NotFoundError("{} not found".format(repository.table))
        logger.info(
            "[RoleService][_check_entity_exist] - "
            "entity %s exist in repository %s",
            entity_id,
            repository.table,
        )

    async def add_role_to_user(
        self, item: UserRoleAction
    ) -> list[RoleResponseModel]:
        await self._check_entity_exist(item.user_id, self.user_repository)
        await self._check_entity_exist(item.role_id, self.role_repository)
        try:
            logger.debug(
                "[RoleService][add_role_to_user] - "
                "trying to add role %s to user %s",
                item.user_id,
                item.role_id,
            )
            await self.user_repository.add_role_to_user(
                item.user_id, item.role_id
            )
        except Exception:
            logger.debug(
                "[RoleService][add_role_to_user] - "
                "failed to add role %s to user %s."
                "Possible role assigned to user.",
                item.user_id,
                item.role_id,
            )
            raise UserRoleActionError(
                "Failed add role to user. "
                "Possible role has already been added."
            )
        result = await self.user_repository.get_user_roles(item.user_id)
        logger.info(
            "[RoleService][add_role_to_user] - "
            "get all assigned to user roles."
        )
        roles = [RoleResponseModel(**role) for role in result]
        logger.info("[RoleService][add_role_to_user] - role assigned to user.")
        return roles

    async def delete_role_from_user(
        self, item: UserRoleAction
    ) -> list[RoleResponseModel]:
        await self._check_entity_exist(item.user_id, self.user_repository)
        await self._check_entity_exist(item.role_id, self.role_repository)

        logger.debug(
            "[RoleService][delete_role_from_user] - "
            "get all assigned to user %s roles.",
            item.user_id,
        )
        user_roles = await self.user_repository.get_user_roles(item.user_id)
        roles_ids = [UUID(role["id"]) for role in user_roles]

        if item.role_id not in roles_ids:
            logger.debug(
                "[RoleService][delete_role_from_user] - "
                "role %s not assigned to user %s.",
                item.user_id,
                item.role_id,
            )
            raise RoleNotAssigned(
                "Role {} not assigned to user {}.".format(
                    item.role_id, item.user_id
                )
            )

        try:
            logger.debug(
                "[RoleService][delete_role_from_user] - "
                "trying to delete role %s from user %s",
                item.user_id,
                item.role_id,
            )
            await self.user_repository.delete_role_from_user(
                item.user_id, item.role_id
            )
        except UserRoleActionError:
            logger.debug(
                "[RoleService][delete_role_from_user] - "
                "failed to delete role %s from user %s.",
                item.user_id,
                item.role_id,
            )
            raise UserRoleActionError(
                "Failed to delete role {} "
                "from user {}. ".format(item.role_id, item.user_id)
            )
        logger.info(
            "[RoleService][delete_role_from_user] - "
            "get all assigned to user roles."
        )
        result = await self.user_repository.get_user_roles(item.user_id)
        roles = [RoleResponseModel(**role) for role in result]
        logger.info(
            "[RoleService][delete_role_from_user] - role deleted from user."
        )
        return roles


@lru_cache
def get_role_service(db: AsyncEngine = Depends(get_postgres)) -> RoleService:
    role_repository = RoleDB(db)
    user_repository = UserDB(db)
    role_srv = RoleService(role_repository, user_repository)
    return role_srv
