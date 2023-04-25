from datetime import datetime
from typing import Callable, Awaitable

from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.api.exceptions.token import NOT_VALID_CREDENTIALS_EXCEPTION, USER_NOT_EXISTS_EXCEPTION, \
    TOKEN_EXPIRED_EXCEPTION
from fastapi_app.api.schemas.token import TokenData
from fastapi_app.database.models import Base
from fastapi_app.database.models.user import UserDB
from fastapi_app.database.utils import get_by_model_value, delete_by_model_value
import pytz


async def verify_token(db: AsyncSession, token_db_model: Base, token: str,
                       data_extractor: Callable[[AsyncSession, str], Awaitable[TokenData | bool]]) -> TokenData | bool:
    """
    :raises TOKEN_EXPIRED_EXCEPTION
    :raises NOT_VALID_CREDENTIALS_EXCEPTION
    :raises USER_NOT_EXISTS_EXCEPTION
    """
    try:
        token_data = await data_extractor(db, token)
        if not token_data:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
    except JWTError:
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    user = await get_by_model_value(db, UserDB, UserDB.username, token_data.username)
    if user is None:
        raise USER_NOT_EXISTS_EXCEPTION
    token_db = await get_by_model_value(db, token_db_model, token_db_model.token_id, token_data.token_id)
    if token_db is None:
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    elif token_db.date_expires < pytz.UTC.localize(datetime.utcnow()):
        await delete_by_model_value(db, token_db_model, token_db_model.token_id, token_db.token_id)
        await db.commit()
        raise TOKEN_EXPIRED_EXCEPTION
    return token_data
