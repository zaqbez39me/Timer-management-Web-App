from datetime import datetime
from typing import Awaitable, Callable

import pytz
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.api.exceptions.token import (NOT_VALID_CREDENTIALS_EXCEPTION,
                                              TOKEN_EXPIRED_EXCEPTION,
                                              USER_NOT_EXISTS_EXCEPTION)
from fastapi_app.api.schemas.session import SessionUser
from fastapi_app.api.schemas.token import TokenData
from fastapi_app.cache import redis_client
from fastapi_app.database.models import Base
from fastapi_app.database.models.user import SessionDB, UserDB
from fastapi_app.database.utils import (delete_by_model_value,
                                        get_by_model_value)


async def verify_token(
    db: AsyncSession,
    token_db_model: Base,
    token: str,
    session_id: str,
    data_extractor: Callable[[AsyncSession, str, str], Awaitable[TokenData | bool]],
) -> TokenData | bool:
    """
    :raises TOKEN_EXPIRED_EXCEPTION
    :raises NOT_VALID_CREDENTIALS_EXCEPTION
    :raises USER_NOT_EXISTS_EXCEPTION
    """
    try:
        token_data = await data_extractor(db, token, session_id)
        if not token_data:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        session = await get_by_model_value(
            db, SessionDB, SessionDB.session_id, token_data.session_id
        )
        if not session:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        await redis_client.set_async(
            name=f"session:{session.session_id}",
            value=SessionUser(user_id=session.user_id),
        )
        if pytz.UTC.localize(dt=token_data.datetime_expires) < pytz.UTC.localize(
            dt=datetime.utcnow()
        ):
            await delete_by_model_value(
                db, token_db_model, token_db_model.token_id, token_data.token_id
            )
            await db.commit()
            raise TOKEN_EXPIRED_EXCEPTION
    except JWTError:
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    user = await get_by_model_value(db, UserDB, UserDB.user_id, session.user_id)
    if user is None:
        raise USER_NOT_EXISTS_EXCEPTION
    token_db = await get_by_model_value(
        db, token_db_model, token_db_model.token_id, token_data.token_id
    )
    if token_db is None:
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    return token_data
