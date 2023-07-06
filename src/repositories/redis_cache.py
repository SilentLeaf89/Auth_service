from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from core.get_logger import logger
from db.redis import get_cache
from repositories.abstract_cache import AbstractCache
from utils.decorators import redis_backoff


class CacheRedis(AbstractCache):
    def __init__(self, client: Redis):
        self._client = client

    @redis_backoff
    async def add_denied_token(self, jti: str, user_id: str, expire: int):
        await self._client.set(name=jti, value=user_id, ex=expire)
        logger.info("{0} set to redis".format(jti))

    @redis_backoff
    async def get(self, jti: str):
        denied_token = await self._client.get(jti)
        logger.info("Try get {0} from redis".format(jti))
        return denied_token

    @redis_backoff
    async def close(self):
        await self._client.close()


@lru_cache
def get_cache_service(
    client: AbstractCache = Depends(get_cache),
) -> AbstractCache:
    return CacheRedis(client)
