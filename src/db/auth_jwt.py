from typing import Optional

from async_fastapi_jwt_auth import AuthJWT

auth_jwt: Optional[AuthJWT] = None


async def get_auth_jwt() -> AuthJWT:
    return auth_jwt
