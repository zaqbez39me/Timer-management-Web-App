from fastapi_app.api.settings import redis_settings, secret_settings
from fastapi_app.cache.client import RedisClient

redis_client = RedisClient(
    host=redis_settings.redis_host,
    password=secret_settings.redis_secret,
    port=redis_settings.redis_port,
)
