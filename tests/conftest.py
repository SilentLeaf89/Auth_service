import psycopg2
from redis import Redis

from tests.config.settings import dsn, test_settings

# Specify pytest plugins for other fixtures
pytest_plugins = [
    "tests.fixtures.redis",
    "tests.fixtures.requests",
    "tests.fixtures.delete_users",
    "tests.fixtures.signup_user",
    "tests.fixtures.get_all_users",
]


def start_redis():
    return Redis(host=test_settings.REDIS_HOST, port=test_settings.REDIS_PORT)


def insert_test_data():
    # Connect to db
    conn = psycopg2.connect(
        host=dsn.host, database=dsn.dbname, user=dsn.user, password=dsn.password
    )

    # create a cursor
    cur = conn.cursor()

    # Insert superadmin user
    cur.execute(
        "INSERT INTO public.user (id, created_at, login, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            "c2b9c859-9803-4d60-9a06-956f33ffec47",
            "2023-07-06 00:30:42.384",
            "superadmin",
            "$2b$12$uPumZKgy8ePuDHK5e4VW.udZZ55niONG7s8MepAs8tqabOEoRgceS",
            "Super",
            "Admin",
        ),
    )
    cur.execute(
        "INSERT INTO public.role (id, created_at, name, access) VALUES (%s, %s, %s, %s)",
        (
            "0c0c4672-dc96-442b-a634-e548eafd91c0",
            "2023-07-06 00:30:42.108",
            "superadmin",
            "superadmin",
        ),
    )
    cur.execute(
        "INSERT INTO public.user_role (user_id, role_id) VALUES (%s, %s)",
        (
            "c2b9c859-9803-4d60-9a06-956f33ffec47",
            "0c0c4672-dc96-442b-a634-e548eafd91c0",
        ),
    )
    cur.execute(
        "INSERT INTO public.role (name, access, id, created_at) VALUES (%s, %s, %s, %s)",
        (
            "test-role-user-delete",
            "test-delete-from-user",
            "34962672-0a64-4e36-b893-96899142c4d8",
            "2023-07-06T00:08:07.496008",
        ),
    )
    cur.execute(
        "INSERT INTO public.user_role (user_id, role_id) VALUES (%s, %s)",
        (
            "c2b9c859-9803-4d60-9a06-956f33ffec47",
            "34962672-0a64-4e36-b893-96899142c4d8",
        ),
    )

    # Insert test roles
    cur.execute(
        "INSERT INTO public.role (name, access, id, created_at) VALUES (%s, %s, %s, %s)",
        (
            "test-role",
            "test-access",
            "34962672-0a64-4e36-b893-96899142c4d4",
            "2023-07-06T00:08:07.496008",
        ),
    )
    cur.execute(
        "INSERT INTO public.role (name, access, id, created_at) VALUES (%s, %s, %s, %s)",
        (
            "delete-role",
            "delete-access",
            "34962672-0a64-4e36-b893-96899142c4d5",
            "2023-07-06T00:08:07.496008",
        ),
    )

    # Close cursor
    conn.commit()
    cur.close()


def empty_db():
    # Connect to db
    conn = psycopg2.connect(
        host=dsn.host, database=dsn.dbname, user=dsn.user, password=dsn.password
    )

    # create a cursor
    cur = conn.cursor()

    # Empty all tables in database
    cur.execute("DELETE FROM public.user_history CASCADE")
    cur.execute("DELETE FROM public.user_role CASCADE")
    cur.execute("DELETE FROM public.refresh_token CASCADE")
    cur.execute("DELETE FROM public.role CASCADE")
    cur.execute("DELETE FROM public.user CASCADE")

    # Close cursor
    conn.commit()
    cur.close()


def pytest_configure():
    # Start redis client
    redis_client = start_redis()

    # Delete all keys in redis
    redis_client.flushall()

    # Close redis client
    redis_client.close()

    # Empty db before insertion
    empty_db()

    # Insert test data
    insert_test_data()


def pytest_unconfigure():
    # Start redis client
    redis_client = start_redis()

    # Delete all keys in redis
    redis_client.flushall()

    # Close redis client
    redis_client.close()

    # Empty db
    empty_db()
