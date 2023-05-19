from fastapi_app.api.schemas.session import SessionUser
from fastapi_app.cache import redis_client
from fastapi_app.database.models.user import SessionDB
from fastapi_app.database.utils import get_by_model_value


async def session_validate(pg, session_id):
    if session_id:
        redis = await redis_client.get_async(name=f"session:{session_id}", model=SessionUser)
        if redis:
            return True
        session_db = await get_by_model_value(
            pg, SessionDB, SessionDB.session_id, session_id
        )
        if session_db:
            await redis_client.set_async(
                name=f"session:{session_id}",
                value=SessionUser(user_id=session_db.user_id),
            )
            return True

    return False
