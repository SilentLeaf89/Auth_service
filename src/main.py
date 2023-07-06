from contextlib import asynccontextmanager

import uvicorn
from async_fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from passlib.context import CryptContext
from redis.asyncio import Redis
from redis.exceptions import RedisError

from sqlalchemy.ext.asyncio import create_async_engine

from api.v1 import auth, role, user
from core.config import (
    auth_settings,
    postgres_settings,
    project_settings,
    redis_setttings,
)
from core.exceptions import (
    redis_connection_exception_handler,
    add_role_error_exception,
    role_not_assigned_exception,
    not_found_exception,
    already_exist_exception,
    unauthorized_exception,
    denied_exception,
)
from db import auth_jwt, postgres, pwd_context, redis
from utils.db import construct_db_url
from utils.exceptions import (
    UserRoleActionError,
    RoleNotAssigned,
    NotFoundError,
    AlreadyExistError,
    PermissionDeniedException,
    UnauthorisedException,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auth JWT
    auth_jwt.auth_jwt = AuthJWT()

    # Crypto Context
    pwd_context.pwd_context = CryptContext(
        schemes=["bcrypt"], deprecated="auto"
    )

    # Redis
    redis.redis = Redis(
        host=redis_setttings.REDIS_HOST, port=redis_setttings.REDIS_PORT
    )

    # Postgres
    # Construct database URL
    db_url = construct_db_url(
        user=postgres_settings.POSTGRES_USER,
        password=postgres_settings.POSTGRES_PASSWORD,
        host=postgres_settings.POSTGRES_HOST,
        port=postgres_settings.POSTGRES_PORT,
        database=postgres_settings.POSTGRES_DATABASE,
    )
    postgres.postgres = create_async_engine(db_url, echo=True, future=True)

    yield

    await redis.redis.close()
    await postgres.postgres.dispose()


app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=project_settings.PROJECT_NAME,
    # Адрес документации в красивом интерфейсе
    docs_url="/api/openapi",
    # Адрес документации в формате OpenAPI
    openapi_url="/api/openapi.json",
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сереализатор на более шуструю версию,
    # написанную на Rust
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(role.router, prefix="/api/v1/role")
app.include_router(user.router, prefix="/api/v1/user")


@AuthJWT.load_config
def get_config():
    return auth_settings


app.add_exception_handler(RedisError, redis_connection_exception_handler)
app.add_exception_handler(UserRoleActionError, add_role_error_exception)
app.add_exception_handler(RoleNotAssigned, role_not_assigned_exception)
app.add_exception_handler(NotFoundError, not_found_exception)
app.add_exception_handler(AlreadyExistError, already_exist_exception)
app.add_exception_handler(UnauthorisedException, unauthorized_exception)
app.add_exception_handler(PermissionDeniedException, denied_exception)


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
