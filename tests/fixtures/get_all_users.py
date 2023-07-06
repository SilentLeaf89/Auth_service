import psycopg
import pytest_asyncio

from tests.config.settings import dsn


@pytest_asyncio.fixture
async def get_all_users():
    async def inner():
        dsn_postgres = "dbname={0} user={1} password={2} host={3} port={4}".format(
            dsn.dbname, dsn.user, dsn.password, dsn.host, dsn.port
        )
        async with await psycopg.AsyncConnection.connect(dsn_postgres) as aconn:
            async with aconn.cursor() as acur:
                await acur.execute("""SELECT * FROM "user";""")
                return await acur.fetchall()

    return inner
