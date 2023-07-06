from typing import Optional

from redis.asyncio import Redis

redis: Optional[Redis] = None


async def get_cache() -> Redis:
    return redis
