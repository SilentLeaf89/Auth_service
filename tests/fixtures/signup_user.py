import uuid
from datetime import datetime

import psycopg
import pytest_asyncio
from passlib.context import CryptContext

from tests.config.settings import dsn


@pytest_asyncio.fixture
async def signup_user():
    async def inner(login: str, password: str, first_name: str, last_name: str):
        dsn_postgres = "dbname={0} user={1} password={2} host={3} port={4}".format(
            dsn.dbname, dsn.user, dsn.password, dsn.host, dsn.port
        )
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        async with await psycopg.AsyncConnection.connect(dsn_postgres) as aconn:
            async with aconn.cursor() as acur:
                await acur.execute(
                    """INSERT INTO "user"
                    (id, created_at, login, password, first_name, last_name)
                    VALUES (%s, %s, %s, %s, %s, %s);""",
                    (
                        uuid.uuid4(),
                        datetime.utcnow(),
                        login,
                        context.hash(password),
                        first_name,
                        last_name,
                    ),
                )

    return inner
