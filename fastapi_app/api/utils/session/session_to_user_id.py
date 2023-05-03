from fastapi_app.api.schemas.session import SessionUser
from fastapi_app.cache import redis_client
from fastapi_app.database.models.user import SessionDB
from fastapi_app.database.utils import get_by_model_value


async def session_to_user_id(db, session_id):
    redis_user = await redis_client.get_async(name=f"session:{session_id}", model=SessionUser)
    if redis_user:
        return redis_user.user_id
    session_db = await get_by_model_value(
        db, SessionDB, SessionDB.session_id, session_id
    )
    await redis_client.set_async(
        name=f"session:{session_id}", value=SessionUser(user_id=session_db.user_id)
    )
    return session_db.user_id
