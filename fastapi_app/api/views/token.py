from fastapi import APIRouter, Cookie, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from fastapi_app.api import jwt_authenticator, oauth2_scheme
from fastapi_app.api.exceptions import get_response_schema
from fastapi_app.api.exceptions.errors.token import TokenError401
from fastapi_app.api.exceptions.token import (NOT_VALID_CREDENTIALS_EXCEPTION,
                                              USER_NOT_EXISTS_EXCEPTION)
from fastapi_app.api.schemas.token import TokenData
from fastapi_app.api.utils.session import session_validate
from fastapi_app.api.utils.token import (verify_access_token,
                                         verify_refresh_token)
from fastapi_app.database import db_engine
from fastapi_app.database.models.user import SessionDB, UserDB
from fastapi_app.database.utils import db_model_to_schema, get_by_model_value

token_router = APIRouter(tags=["token"], prefix="/token")


@token_router.get(
    "/access/info",
    response_model=TokenData,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_401_UNAUTHORIZED: get_response_schema(TokenError401)},
)
async def get_access_token_info(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(db_engine.session),
    session_id: str | None = Cookie(default=None),
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, token, session_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(token_data))


@token_router.get(
    "/refresh/info",
    response_model=TokenData,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_401_UNAUTHORIZED: get_response_schema(TokenError401)},
)
async def get_refresh_token_info(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(db_engine.session),
    session_id: str | None = Cookie(default=None),
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_refresh_token(token, db, session_id)
    return token_data


@token_router.post(
    "/refresh",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenData,
    responses={status.HTTP_401_UNAUTHORIZED: get_response_schema(TokenError401)},
)
async def get_new_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(db_engine.session),
    session_id: str | None = Cookie(default=None),
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_refresh_token(token, db, session_id)
    session_db = await get_by_model_value(
        db, SessionDB, SessionDB.session_id, token_data.session_id
    )
    user_db = await get_by_model_value(db, UserDB, UserDB.user_id, session_db.user_id)
    if not user_db:
        raise USER_NOT_EXISTS_EXCEPTION
    new_access_token = await jwt_authenticator.create_access_token(db, session_id)
    return await jwt_authenticator.get_access_token_data(db, new_access_token, session_id)
