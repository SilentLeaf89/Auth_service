import backoff
from redis import Redis
from redis.exceptions import ConnectionError

from config.logger import get_logger

logger = get_logger(__name__)


@backoff.on_exception(backoff.expo, ConnectionError, logger=logger)
def wait_for_redis(redis_client_host: str):
    redis_client = Redis(redis_client_host, socket_connect_timeout=1)
    if redis_client.ping():
        logger.debug("Connection to Redis is successful!")
