from config.settings import test_settings
from unit.utils.wait_for_redis import wait_for_redis

if __name__ == "__main__":
    wait_for_redis(redis_client_host=test_settings.REDIS_HOST)
