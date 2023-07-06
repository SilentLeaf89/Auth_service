from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine

postgres: Optional[AsyncEngine] = None


def get_postgres() -> AsyncEngine:
    return postgres
