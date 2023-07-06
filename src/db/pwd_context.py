from typing import Optional

from passlib.context import CryptContext

pwd_context: Optional[CryptContext] = None


async def get_pwd_context() -> CryptContext:
    return pwd_context
