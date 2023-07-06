import pytest_asyncio
from redis import Redis

from tests.config.settings import test_settings


@pytest_asyncio.fixture
async def get_redis():
    client_redis = Redis(host=test_settings.REDIS_HOST, port=test_settings.REDIS_PORT)
    client_redis.flushall()
    yield client_redis
    client_redis.close()
