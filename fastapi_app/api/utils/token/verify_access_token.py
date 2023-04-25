from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.api import jwt_authenticator
from fastapi_app.api.schemas.token import TokenData
from fastapi_app.api.utils.token.verify_token import verify_token
from fastapi_app.database.models.token import AccessTokenDB


async def verify_access_token(db: AsyncSession, token: str) -> TokenData | bool:
    return await verify_token(db, AccessTokenDB, token, jwt_authenticator.get_access_token_data)
