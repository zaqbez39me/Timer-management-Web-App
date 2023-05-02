from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.api import jwt_authenticator
from fastapi_app.api.schemas.token import TokenData
from fastapi_app.api.utils.token.verify_token import verify_token
from fastapi_app.database.models.token import RefreshTokenDB


async def verify_refresh_token(
    token: str, db: AsyncSession, session_id: str
) -> TokenData | bool:
    return await verify_token(
        db, RefreshTokenDB, token, session_id, jwt_authenticator.get_refresh_token_data
    )
