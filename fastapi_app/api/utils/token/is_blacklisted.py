from fastapi_app.api.schemas.token.blacklist_token import TokenBlacklist
from fastapi_app.cache import redis_client


async def is_blacklisted(token):
    if await redis_client.get(f"blacklist:{token}", model=TokenBlacklist):
        return True
    return False
