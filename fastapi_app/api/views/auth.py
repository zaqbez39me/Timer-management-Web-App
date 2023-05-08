import uuid
from datetime import datetime

import pytz
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.params import Cookie, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from fastapi_app.api import (jwt_authenticator, oauth2_scheme, password_hasher,
                             user_authenticator)
from fastapi_app.api.exceptions import get_response_schema
from fastapi_app.api.exceptions.errors.user_change_password import \
    UserChangePasswordError401
from fastapi_app.api.exceptions.errors.user_login import UserLoginError401
from fastapi_app.api.exceptions.errors.user_logout.error_401 import \
    UserLogoutError401
from fastapi_app.api.exceptions.errors.user_me import UserMeError401
from fastapi_app.api.exceptions.errors.user_register import \
    UserRegisterError409
from fastapi_app.api.exceptions.token import NOT_VALID_CREDENTIALS_EXCEPTION
from fastapi_app.api.exceptions.user import (
    USER_CREDENTIALS_ARE_INVALID_EXCEPTION, USER_USERNAME_OCCUPIED_EXCEPTION)
from fastapi_app.api.schemas.auth.requests import UserChangePasswordRequest
from fastapi_app.api.schemas.auth.responses import (LoginResponse,
                                                    LogoutResponse,
                                                    RegistrationResponse,
                                                    UserChangePasswordResponse,
                                                    UserMeResponse)
from fastapi_app.api.schemas.session import SessionUser
from fastapi_app.api.schemas.user import UserModel
from fastapi_app.api.utils.session import session_validate
from fastapi_app.api.utils.session.session_to_user_id import session_to_user_id
from fastapi_app.api.utils.token import verify_access_token
from fastapi_app.cache import redis_client
from fastapi_app.database import db_engine
from fastapi_app.database.models.token import RefreshTokenDB
from fastapi_app.database.models.user import SessionDB, UserDB
from fastapi_app.database.utils import (add_to_db, db_model_to_schema,
                                        get_by_model_value)

auth_router = APIRouter(tags=["auth"], prefix="/auth")


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegistrationResponse,
    responses={status.HTTP_409_CONFLICT: get_response_schema(UserRegisterError409)},
)
async def register(
        username: Annotated[constr(min_length=1, max_length=20), Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(db_engine.session),
):
    res = await get_by_model_value(db, UserDB, UserDB.username, username)
    if not res:
        user_db = await user_authenticator.register_new_user(db, username, password)
        user = db_model_to_schema(user_db, UserModel)
        response = RegistrationResponse(
            **user.__dict__, message="User Created Successfully."
        )
        return response
    raise USER_USERNAME_OCCUPIED_EXCEPTION


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses={status.HTTP_401_UNAUTHORIZED: get_response_schema(UserLoginError401)},
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
):
    user_db = await user_authenticator.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user_db:
        raise USER_CREDENTIALS_ARE_INVALID_EXCEPTION
    user = db_model_to_schema(user_db, UserModel)
    if not session_id or not await session_validate(db, session_id):
        session_id = str(uuid.uuid4())
        await redis_client.set_async(
            name=f"session:{session_id}", value=SessionUser(user_id=user_db.user_id)
        )
        await add_to_db(
            session=db,
            item=SessionDB(session_id=session_id, user_id=user_db.user_id),
            commit=True,
        )
    response_dict = await jwt_authenticator.create_tokens(db=db, session_id=session_id)
    response_dict.update({"data": user, "token_type": "bearer"})
    response = LoginResponse(**response_dict, message="User Logged in successfully.")
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(response)
    )
    response.set_cookie(key="session_id", value=session_id)
    return response


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=LogoutResponse,
    responses={status.HTTP_401_UNAUTHORIZED: get_response_schema(UserLogoutError401)},
)
async def logout(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    access_token_data = await verify_access_token(db, token, session_id)
    if access_token_data:
        user_id = await session_to_user_id(db, session_id)
        refresh_token = await get_by_model_value(
            db, RefreshTokenDB, RefreshTokenDB.session_id, session_id
        )
        refresh_token_data = (
            await jwt_authenticator.get_refresh_token_data_no_validation(
                refresh_token.refresh_token
            )
        )
        access_expires = pytz.UTC.localize(dt=access_token_data.datetime_expires) - pytz.UTC.localize(
            dt=datetime.utcnow()
        )
        refresh_expires = refresh_token_data.datetime_expires - pytz.UTC.localize(
            dt=datetime.utcnow()
        )
        await jwt_authenticator.add_to_blacklist(
            access_token_data.token, user_id, access_expires
        )
        await jwt_authenticator.add_to_blacklist(
            refresh_token_data.token, user_id, refresh_expires
        )
    return LogoutResponse(message="Logged out successfully!")


@auth_router.get(
    "/user/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeResponse,
    responses={status.HTTP_401_UNAUTHORIZED: get_response_schema(UserMeError401)},
)
async def get_user_me(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, token, session_id)
    if token_data:
        user_id = await session_to_user_id(db, session_id)
        user_db = await get_by_model_value(db, UserDB, UserDB.user_id, user_id)
        user = db_model_to_schema(user_db, UserModel)
        response = UserMeResponse(user=user, message="User information report.")
        return response
    raise NOT_VALID_CREDENTIALS_EXCEPTION


async def change_password_no_auth(db, user_db, new_password):
    user_db.hashed_password = await password_hasher.get_password_hash(
        new_password
    )
    await db.commit()


@auth_router.post(
    "/user/change-password",
    status_code=status.HTTP_200_OK,
    response_model=UserChangePasswordResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_response_schema(UserChangePasswordError401)
    },
)
async def change_password(
        request: UserChangePasswordRequest,
        token: Annotated[str, Depends(oauth2_scheme)],
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    user_db = await jwt_authenticator.authenticate_user(
        db, token, request.old_password, session_id=session_id
    )
    background_tasks.add_task(change_password_no_auth, db, user_db, request.new_password)
    user = db_model_to_schema(user_db, UserModel)
    response = UserChangePasswordResponse(
        user=user, message="Changed password successfully."
    )
    return response
