from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Request
from fastapi.responses import ORJSONResponse

from utils.exceptions import (
    UserRoleActionError,
    RoleNotAssigned,
    NotFoundError,
    AlreadyExistError,
    UnauthorisedException,
    PermissionDeniedException,
)


async def redis_connection_exception_handler(request, exc):
    return ORJSONResponse(
        status_code=503, content={"detail": "Redis service unavailable"}
    )


async def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return ORJSONResponse(
        status_code=exc.status_code, content={"detail": exc.message}
    )


async def add_role_error_exception(request: Request, exc: UserRoleActionError):
    return ORJSONResponse(
        status_code=422,
        content={"detail": exc.message},
    )


async def role_not_assigned_exception(request: Request, exc: RoleNotAssigned):
    return ORJSONResponse(
        status_code=422,
        content={"detail": exc.message},
    )


async def not_found_exception(request: Request, exc: NotFoundError):
    return ORJSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


async def already_exist_exception(request: Request, exc: AlreadyExistError):
    return ORJSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


async def unauthorized_exception(request: Request, exc: UnauthorisedException):
    return ORJSONResponse(
        status_code=401,
        content={"detail": exc.message},
    )


async def denied_exception(request: Request, exc: PermissionDeniedException):
    return ORJSONResponse(
        status_code=403,
        content={"detail": exc.message},
    )
