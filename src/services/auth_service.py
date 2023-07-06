import datetime
from functools import lru_cache
from http import HTTPStatus
from typing import Optional, Tuple


from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from db.postgres import get_postgres
from core.get_logger import logger
from models.user import User
from models.user_history import UserHistory
from models.refresh_token import RefreshToken
from repositories.abstract_cache import AbstractCache
from repositories.redis_cache import get_cache_service
from repositories.refresh_token_db import RefreshTokenDB
from repositories.user_db import UserDB
from repositories.user_history_db import UserHistoryDB
from schemas.user import UserCreate, UserHistoryShow, UserHistoryAdd
from schemas.login import Login, Change
from services.abstract_password_services import AbstractPasswordService
from services.abstract_service import AbstractService
from services.password_service import get_password_service
from utils.constants import AdminRole
from utils.exceptions import UnauthorisedException, PermissionDeniedException


class AuthService(AbstractService):
    def __init__(
        self,
        cache_repository: AbstractCache,
        user_repository: UserDB,
        user_history: UserHistoryDB,
        token_repository: RefreshTokenDB,
        password_service: AbstractPasswordService,
        authorize_service: AuthJWT,
    ) -> None:
        self.cache_repository = cache_repository
        self.user_repository = user_repository
        self.user_history = user_history
        self.password_service = password_service
        self.Authorize = authorize_service
        self.token_repository = token_repository

    async def signup(self, user_create: UserCreate) -> dict[str, str]:
        """Singup user

        Args:
            user_create (UserCreate): user signup data

        Returns:
            dict[str, str]: user creation message
        """
        logger.debug("def 'signup' run with %s", user_create)
        user_db = User(**user_create.dict())
        # Захешировать пароль
        user_db.password = self.password_service.get_password_hash(
            user_db.password
        )
        await self.create_free_login(user_db)
        logger.info("User %s create successful", user_db)

        return {"msg": "User {} create successful".format(user_create.login)}

    async def refresh(self) -> dict[str, str]:
        """Refresh access_token

        Returns:
            dict[str, str]: "access_token": <refresh access_token>
        """
        logger.debug("def 'refresh' run")

        await self.check_refresh_token()

        user_id = await self.Authorize.get_jwt_subject()
        await self.check_user_in_db(user_id)

        new_access_token = await self.issue_access_token(user_id)

        logger.info(
            "access token has been issued to the user %s", user_id
        )
        return {"access_token": new_access_token}

    async def login(self, login: Login) -> dict[str, str]:
        """User authentication

        Args:
            login (Login): user login data

        Returns:
            dict[str, str]: access and refresh tokens
        """
        logger.debug("def 'login' run with %s", login)

        user = await self.get_user_by_login(login)

        (
            access_token, refresh_token
        ) = await self.issue_access_and_refresh_token(user.id)

        refresh_token_db = RefreshToken(
            token=refresh_token, user_id=str(user.id)
        )
        await self.token_repository.insert(entity=refresh_token_db)

        await self.add_event(user.id, "Account logged in")

        logger.info(
            "access and refresh token has been issued for %s", user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def logout(self) -> dict[str, str]:
        """User logout

        Returns:
            dict[str, str]: user logout message
        """
        logger.debug("def 'logout' run")

        await self.check_access_token()

        user_id = await self.Authorize.get_jwt_subject()

        await self.add_token_to_denied(user_id)

        await self.token_repository.delete(entity_id=user_id)
        await self.Authorize.unset_jwt_cookies()

        await self.add_event(user_id, "Account logged out")

        logger.info("%s was logged out", user_id)
        return {"msg": "logged out successful"}

    async def change(self, change: Change) -> dict[str, str]:
        """Change login and (or) password for user

        Args:
            change (Change): user change data

        Returns:
            dict[str, str]: user change message
        """
        logger.debug("def 'change' run with %s", change)
        await self.check_access_token()

        await self.check_denied_token()

        user_id = await self.Authorize.get_jwt_subject()
        user = (await self.user_repository.get(entity_id=user_id))[0]

        self.verify_password_on_change(change, user, user_id)

        await self.update_new_entity(change, user, user_id)

        logger.info("login and (or) password %s has been change", user_id)
        return {"msg": "login and (or) password has been change"}

  
    async def history(
        self,
        n_items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        descending: Optional[bool] = None,
    ) -> list[UserHistoryShow]:
        """Login and logout history

        Returns:
            list[UserHistoryShow]: list events
        """
        # только со свежим access_token
        try:
            await self.Authorize.jwt_required()
        except AuthJWTException:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Unauthorized action",
            )
        logger.debug("def 'history' run")

        await self.check_access_token()

        user_id = await self.Authorize.get_jwt_subject()

        events = []

        # adjust page number if none
        if page_number is None or n_items_per_page is None:
            offset = None
        else:
            offset = n_items_per_page * (page_number - 1)

        user_history = await self.user_history.find(
            {"user_id": user_id},
            offset=offset,
            limit=n_items_per_page,
            order_by=UserHistory.created_at,
            descending=descending,
        )
        for event_history in user_history:
            events.append(
                UserHistoryShow(
                    event=event_history.event,
                    created_at=event_history.created_at,
                )
            )
        logger.info("%s viewed history", user_id)
        return events

    async def get_permissions(self, user_id: UUID) -> list[str]:
        """get user permission
        get all access values for a user by
        concatenating all access values in each user role

        Args:
            user_id (UUID): user id

        Returns:
            list[str]: list of access values
        """
        logger.debug("def 'get_permissions' run with %s", user_id)
        user_roles = await self.user_repository.get_user_roles(user_id)
        access_set = set()
        for role in user_roles:
            access_values = role["access"].split(",")
            for access in access_values:
                access = access.strip()
                access_set.add(access)
        logger.info("permissions has been granted to the %s", user_id)
        return list(access_set)

    async def check_access(self, access_list: list[str]) -> None:
        """Check permission.
        in route you can pass list of permission which must be in
        access field assigned to user role

        Args:
            access_list (list[str]): list of
                permissions separated by comma.

        Raises:
            UnauthorisedException: return 401 when user don't have JWT token
            PermissionDeniedException: if user not authontificated to resource return 403
        """
        logger.debug("def 'check_access' run with %s", access_list)
        try:
            await self.Authorize.jwt_required()
        except AuthJWTException:
            raise UnauthorisedException

        current_user: dict = await self.Authorize.get_raw_jwt()
        user_access_list: list = current_user.get("scope", [])
        if not user_access_list:
            logger.error("%s don't have access to this route", current_user)
            raise PermissionDeniedException(
                "You don't have access to this route."
            )

        if AdminRole.SUPER_ADMIN.value in user_access_list:
            logger.info("granted super admin permission")
            return
        for access in access_list:
            if access not in user_access_list:
                logger.error(
                    "%s don't have permission for %s", current_user, access
                )
                raise PermissionDeniedException("You don't have permission")
        logger.info(
            "%s has received the following permissoins: %s",
            current_user, user_access_list)
        return

    async def check_access_token(self) -> None:
        """Check access_token in headers. If token is valid - continue,
           else raises exception.
        Raises:
            HTTPException: Unauthorized action, access_token not valid.
        """
        logger.debug("def 'check_access_token' run")
        try:
            await self.Authorize.jwt_required()
        except AuthJWTException:
            logger.error("Unauthorized action, access_token not valid")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Unauthorized action",
            )
        logger.info(
            "%s have valid access token",
            await self.Authorize.get_jwt_subject()
        )

    async def check_refresh_token(self) -> None:
        """Check refresh_token in headers. If token is valid - continue,
           else raises exception.

        Raises:
            HTTPException: Unauthorized action, access_token not valid.
        """
        logger.debug("def 'check_refresh_token' run")
        try:
            await self.Authorize.jwt_refresh_token_required()
        except AuthJWTException:
            logger.error("Unauthorized action, refresh_token not valid")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Unauthorized action",
            )
        logger.info(
            "%s have valid refresh token",
            await self.Authorize.get_jwt_subject()
        )

    async def check_denied_token(self) -> None:
        """Сhecks if the token is in the denied list.

        Raises:
            HTTPException: Unauthorized action, access_token in denied list!
                Please note that hacking is possible.
        """
        logger.debug("def 'check_denied_token' run")
        jti = (await self.Authorize.get_raw_jwt())["jti"]
        if await self.cache_repository.get(jti):
            logger.error("Unauthorized action, access_token in denied list!!!")
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Unauthorized action",
            )
        logger.info("%s not in denied lists", jti)

    def verify_password_on_change(self, change: Change, user, user_id) -> None:
        """Verify enter old password with password in database.

        Args:
            change (Change): model include old_password, new_login,
                new_password
            user (User): Model User
            user_id (str|UUID): user identifier

        Raises:
            HTTPException: Incorrect password.
        """
        logger.debug("""def 'verify_password_on_change' run with 'change': %s,
            'user' %s and 'user_id' %s""", change, user, user_id)
        if not self.password_service.verify_password(
            change.old_password, user.password
        ):
            logger.error("""Unauthorized action, incorrect password for
                user %s""", user_id)
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect password",
            )
        logger.info("%s entered password matches", user_id)

    async def update_new_entity(self, change: Change, user, user_id) -> None:
        """Update login or password for user

        Args:
            change (Change): model include old_password, new_login,
                new_password
            user (User): Model user
            user_id (str|UUID): user identifier
        """
        logger.debug("""def 'update_new_entity' run with 'change': %s,
            'user' %s and 'user_id' %s""", change, user, user_id)
        new_password_hash = self.password_service.get_password_hash(
            change.new_password
        )
        new_entity = UserCreate(
            login=change.new_login,
            password=new_password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        await self.user_repository.update(
            entity_id=user_id, new_entity=new_entity
        )
        logger.info("%s has been updated in database", user_id)

    async def create_free_login(self, user_db) -> None:
        """Checks if the entered login is free

        Args:
            user_db (Base): model "User" includes login, password,
                            first_name, last_name

        Raises:
            HTTPException: If user_db already exists in DB
        """
        logger.debug("def 'create_free_login' run with %s", user_db)
        try:
            await self.user_repository.insert(entity=user_db)
        except IntegrityError:
            logger.error("login %s already exists", user_db.login)
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="This login already exists",
            )
        logger.info("%s has been created", user_db.login)

    async def check_user_in_db(self, user_id) -> None:
        """Checks if the user exists in the database

        Args:
            user_id (str|UUID): user identifier

        Raises:
            HTTPException: _description_
        """
        logger.debug("def 'check_user_in_db' run with %s", user_id)
        if len(await self.token_repository.find({"user_id": user_id})) == 0:
            logger.error("Unauthorized action, user %s not found", user_id)
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Unauthorized action",
            )
        logger.info("%s has been found in database", user_id)

    async def issue_access_token(self, user_id) -> str:
        """Issue access_token for user with his scope

        Args:
            user_id (str|UUID): user identifier

        Returns:
            str: new access token
        """
        logger.debug("def 'issue_access_token' run with %s", user_id)
        scope = {"scope": await self.get_permissions(user_id)}
        access_token = await self.Authorize.create_access_token(
            subject=str(user_id),
            user_claims=scope,
        )
        await self.Authorize.set_access_cookies(access_token)
        logger.info("access token has been created for %s", user_id)
        return access_token

    async def issue_refresh_token(self, user_id) -> str:
        """Issue refresh_token for user with his scope

        Args:
            user_id (str|UUID): user identifier

        Returns:
            str: new refresh token
        """
        logger.debug("def 'issue_refresh_token' run with %s", user_id)
        access = {"access": await self.get_permissions(user_id)}
        refresh_token = await self.Authorize.create_refresh_token(
            subject=str(user_id),
            user_claims=access,
        )
        await self.Authorize.set_refresh_cookies(refresh_token)
        logger.info("refresh token has been created for %s", user_id)
        return refresh_token

    async def get_user_by_login(self, login: Login) -> User:
        """Get user (Base) from db if login and password is correct

        Args:
            login (Login): model include login and password fields

        Returns:
            User: Model User
        """
        logger.debug("def 'get_user_by_login' run with %s", login)
        user = await self.user_repository.find({"login": login.login})
        # Сравнить
        if len(user) == 0 or not self.password_service.verify_password(
            login.password, user[0].password
        ):
            logger.error("""Unauthorized action, incorrect username or password
                for input "%s" login """, login.login)
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        logger.info("%s has been received from the database", user[0].id)
        # Получить первый элемент из списка
        return user[0]

    async def issue_access_and_refresh_token(
            self, user_id,
            ) -> Tuple[str, str]:
        """Issue access and refresh token for user

        Args:
            user_id (str|UUID): user identifier

        Returns:
            Tuple[str, str]: access and refresh token
        """
        logger.debug("def 'issue_access_and_refresh_token' run with %s", user_id)
        access_token = await self.issue_access_token(user_id)
        refresh_token = await self.issue_refresh_token(user_id)
        logger.info("access and refresh token has been issued for %s", user_id)
        return (access_token, refresh_token)

    async def add_token_to_denied(self, user_id) -> None:
        """Add token to denied list in cache

        Args:
            user_id (str|UUID): user identifier
        """
        logger.debug("def 'add_token_to_denied' run with %s", user_id)
        denied_token = (await self.Authorize.get_raw_jwt())["jti"]
        now = datetime.datetime.timestamp(datetime.datetime.now())
        expire = int((await self.Authorize.get_raw_jwt())["exp"] - now)

        logger.info("token %s added in denied list", denied_token)
        await self.cache_repository.add_denied_token(
            jti=str(denied_token),
            user_id=user_id,
            expire=expire,
        )

    async def add_event(self, user_id, name: str):
        """Add event to user history

        Args:
            user_id (str|UUID): user identifier
            name (str): event description
        """
        event = UserHistoryAdd(
            user_id=user_id,
            event=name,
        )
        event = UserHistory(**event.dict())
        await self.user_history.insert(entity=event)


@lru_cache
def get_auth_service(
    cache_repository: AbstractCache = Depends(get_cache_service),
    db_connection: AsyncEngine = Depends(get_postgres),
    password_service: AbstractPasswordService = Depends(get_password_service),
    authorize_service: AuthJWT = Depends(),
) -> AuthService:
    return AuthService(
        cache_repository=cache_repository,
        user_repository=UserDB(db_connection),
        user_history=UserHistoryDB(db_connection),
        token_repository=RefreshTokenDB(db_connection),
        password_service=password_service,
        authorize_service=authorize_service,
    )
