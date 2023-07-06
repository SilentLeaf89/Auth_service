import functools

import backoff
from redis.exceptions import RedisError

from core.config import project_settings


def redis_backoff(func):
    @functools.wraps(func)
    @backoff.on_exception(
        backoff.expo, RedisError, max_time=project_settings.BACKOFF_MAX_TIME
    )
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
