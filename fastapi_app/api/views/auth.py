from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing_extensions import Annotated

from fastapi_app.api import user_authenticator, jwt_authenticator, oauth2_scheme, password_hasher
from fastapi_app.api.exceptions import get_response_schema
from fastapi_app.api.exceptions.errors.user_change_password import UserChangePasswordError401
from fastapi_app.api.exceptions.errors.user_login import UserLoginError401
from fastapi_app.api.exceptions.errors.user_me import UserMeError401
from fastapi_app.api.exceptions.errors.user_register import UserRegisterError409
from fastapi_app.api.exceptions.token import NOT_VALID_CREDENTIALS_EXCEPTION
from fastapi_app.api.exceptions.user import USER_CREDENTIALS_ARE_INVALID_EXCEPTION, USER_USERNAME_OCCUPIED_EXCEPTION
from fastapi_app.api.schemas.auth.requests import UserChangePasswordRequest
from fastapi_app.api.schemas.auth.responses import RegistrationResponse, LoginResponse, UserMeResponse, \
    UserChangePasswordResponse
from fastapi_app.api.schemas.user import UserModel
from fastapi_app.api.utils.token import verify_access_token
from fastapi_app.database import db_engine
from fastapi_app.database.models.user import UserDB
from fastapi_app.database.utils import get_by_model_value, db_model_to_schema

auth_router = APIRouter(tags=['auth'], prefix="/auth")


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegistrationResponse,
    responses={
        status.HTTP_409_CONFLICT: get_response_schema(UserRegisterError409)
    }
)
async def register(username: Annotated[constr(min_length=1, max_length=20), Form()],
                   password: Annotated[str, Form()],
                   db: AsyncSession = Depends(db_engine.session)):
    res = await get_by_model_value(db, UserDB, UserDB.username, username)
    if not res:
        user_db = await user_authenticator.register_new_user(db, username,
                                                             password)
        user = db_model_to_schema(user_db, UserModel)
        response = RegistrationResponse(**user.__dict__, message="User Created Successfully.")
        return response
    else:
        raise USER_USERNAME_OCCUPIED_EXCEPTION


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_response_schema(UserLoginError401)
    }
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(db_engine.session)
):
    user_db = await user_authenticator.authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    if not user_db:
        raise USER_CREDENTIALS_ARE_INVALID_EXCEPTION
    user = db_model_to_schema(user_db, UserModel)
    response_dict = await jwt_authenticator.create_tokens(db=db, user=user)
    response_dict.update({"data": user, "token_type": "bearer"})
    response = LoginResponse(**response_dict, message="User Logged in successfully.")
    return response


@auth_router.get(
    "/user/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_response_schema(UserMeError401)
    }
)
async def get_user_me(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(db_engine.session)
):
    token_data = await verify_access_token(db, token)
    if token_data:
        user_db = await get_by_model_value(db, UserDB, UserDB.username, token_data.username)
        user = db_model_to_schema(user_db, UserModel)
        response = UserMeResponse(user=user, message="User information report.")
        return response
    else:
        raise NOT_VALID_CREDENTIALS_EXCEPTION


@auth_router.post(
    "/user/change-password",
    status_code=status.HTTP_200_OK,
    response_model=UserChangePasswordResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_response_schema(UserChangePasswordError401)
    }
)
async def change_password(
        request: UserChangePasswordRequest,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(db_engine.session),
):
    user_db = await jwt_authenticator.authenticate_user(db, token, request.old_password)
    user_db.hashed_password = await password_hasher.get_password_hash(request.new_password)
    user = db_model_to_schema(user_db, UserModel)
    response = UserChangePasswordResponse(user=user, message="Changed password successfully.")
    await db.commit()
    return response
