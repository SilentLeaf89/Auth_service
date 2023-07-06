import asyncio

import typer

from passlib.context import CryptContext
from typing_extensions import Annotated
from typing import Optional

from core.get_logger import get_logger
from repositories.user_db import UserDB
from repositories.role_db import RoleDB
from services.user_service import UserService
from services.password_service import PasslibPasswordService
from services.role_service import RoleService
from schemas.user import UserCreate, UserRoleAction
from schemas.role import RoleModel
from utils.commands import pg_engine
from utils.constants import AdminRole

cli = typer.Typer()


@cli.command()
def add_superuser(
    login: Annotated[str, typer.Option(help="superuser login")],
    password: Annotated[
        str,
        typer.Option(help="superuser password", hide_input=True, prompt=True),
    ],
    firstname: Annotated[
        Optional[str], typer.Option(help="superuser first name")
    ] = None,
    lastname: Annotated[
        Optional[str], typer.Option(help="superuser last name")
    ] = None,
) -> None:
    loop = asyncio.get_event_loop()

    async def add_superuser_async():
        """Create new user with superadmin role

        Returns:
            message: result of user creation
        """
        logger = get_logger()

        logger.debug(
            "[CLI][add_superuser_async] - Create superuser login: %s.", login
        )

        # инициализация репозиториев и сервисов
        user_repository = UserDB(pg_engine)
        role_repository = RoleDB(pg_engine)
        pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        pass_service = PasslibPasswordService(pass_context)

        role_service = RoleService(role_repository, user_repository)
        user_service = UserService(user_repository, pass_service)

        # заполнение схем pydantic user и role
        admin_role = RoleModel(
            name=AdminRole.SUPER_ADMIN.value,
            access=AdminRole.SUPER_ADMIN.value,
        )

        new_user = UserCreate(
            login=login,
            password=password,
            first_name=firstname,
            last_name=lastname,
        )

        # если роль с уникальным значением имени уже есть, берем ее
        result_role = await role_service.find(admin_role.name)
        # если нет, создаем новую
        if not result_role:
            result_role = await role_service.add(admin_role)

        # создаем пользователя
        result_user = await user_service.add(new_user)

        # если пользователь None то он уже есть в базе, заканчиваем с ошибкой
        if not result_user:
            return None

        # заполняем схему pydantic из найденных значений
        assign_model = UserRoleAction(
            user_id=result_user.id, role_id=result_role.id
        )
        # привязываем роль суперпользователя нашему пользователю
        result_assign = await role_service.add_role_to_user(assign_model)

        # успешно если есть любое значение в результате
        if result_assign:
            logger.info(
                "[CLI][add_superuser_async] - superuser %s created.",
                new_user.login,
            )
            return

        logger.debug("Failed to create superuser %s.", new_user.login)

    loop.run_until_complete(add_superuser_async())


if __name__ == "__main__":
    cli()
