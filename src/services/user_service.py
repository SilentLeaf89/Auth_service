from functools import lru_cache
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncEngine

from db.postgres import get_postgres
from core.get_logger import logger
from repositories.user_db import UserDB
from services.abstract_password_services import AbstractPasswordService
from services.password_service import get_password_service
from schemas.user import UserSchema, UserCreate


class UserService:
    def __init__(
        self,
        user_repository: UserDB,
        password_service: AbstractPasswordService,
    ) -> None:
        self.user_repository = user_repository
        self.password_service = password_service

    async def find_by_login(self, login: str) -> UserSchema | None:
        logger.debug(
            "[UserService][find_by_login] - "
            "trying to find user by login %s",
            login,
        )
        result = await self.user_repository.find({"login": login})
        if not result:
            logger.debug(
                "[UserService][find_by_login] - login %s not found",
                login,
            )
            return None
        logger.info(
            "[UserService][find_by_login] - user found by login ",
        )
        return UserSchema.from_orm(result[0])

    async def add(self, user_create: UserCreate) -> UserSchema | None:
        if await self.find_by_login(user_create.login):
            return None
        logger.debug(
            "[UserService][add] - trying to add user %s",
            user_create.login,
        )
        password = self.password_service.get_password_hash(
            user_create.password
        )
        user_create.password = password
        result = await self.user_repository.insert(entity=user_create)
        if not result:
            logger.debug(
                "[UserService][add] - add user %s failed",
                user_create.login,
            )
            return None
        logger.info("[UserService][add] - user added")
        return UserSchema.from_orm(result[0])


@lru_cache
def get_user_service(
    db: AsyncEngine = Depends(get_postgres),
    pass_service: AbstractPasswordService = Depends(get_password_service),
) -> UserService:
    user_repository = UserDB(db)
    pass_service = pass_service
    return UserService(user_repository, pass_service)
