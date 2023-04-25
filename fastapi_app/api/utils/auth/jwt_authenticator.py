from copy import deepcopy
from datetime import datetime

import pytz
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.api import settings
from fastapi_app.api.exceptions.token import NOT_VALID_CREDENTIALS_EXCEPTION, USER_NOT_EXISTS_EXCEPTION, \
    TOKEN_EXPIRED_EXCEPTION
from fastapi_app.api.exceptions.user import USER_PASSWORD_INVALID_EXCEPTION
from fastapi_app.api.schemas.token import TokenData
from fastapi_app.api.schemas.user import UserModel
from fastapi_app.api.utils.auth.password_hashing import PasswordHasher
from fastapi_app.database.models import Base
from fastapi_app.database.models.token import AccessTokenDB, RefreshTokenDB
from fastapi_app.database.models.user import UserDB
from fastapi_app.database.utils import delete_by_model_value, get_by_model_value


class JWTAuthenticator:
    def __init__(self, access_secret_key: str, refresh_secret_key: str, algorithm, access_expiration_time,
                 refresh_expiration_time):
        self.password_hasher = PasswordHasher(settings.password_schemes)
        self.jwt_access_secret: str = access_secret_key
        self.jwt_refresh_secret: str = refresh_secret_key
        self.algorithm = algorithm
        self.access_expiration_time = access_expiration_time
        self.refresh_expiration_time = refresh_expiration_time

    async def create_tokens(self, db: AsyncSession, user: UserModel) -> dict:
        encoded_jwt_access = await self.create_access_token(db=db, user=user)
        encoded_jwt_refresh = await self.create_refresh_token(db=db, user=user)
        return {"access_token": encoded_jwt_access, "refresh_token": encoded_jwt_refresh}

    async def get_access_token_data(self, db: AsyncSession, token: str) -> TokenData | bool:
        return await self.__get_token_data(db, AccessTokenDB, token, self.jwt_access_secret)

    async def get_refresh_token_data(self, db: AsyncSession, token: str) -> TokenData | bool:
        return await self.__get_token_data(db, RefreshTokenDB, token, self.jwt_refresh_secret)

    async def __get_token_data(self, db: AsyncSession, db_model: Base, token: str, secret: str) -> TokenData | bool:
        try:
            payload = jwt.decode(token, secret, algorithms=[self.algorithm])
        except JWTError:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        username: str = payload.get("sub")
        if not username:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        token_db = await get_by_model_value(db, db_model, db_model.token_id, payload.get("id"))
        if not token_db:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        token_data = TokenData(token_id=token_db.token_id, username=username, token=token,
                               datetime_expires=token_db.date_expires, token_type="bearer")
        return token_data

    async def create_access_token(self, db: AsyncSession, user: UserModel):
        user_id, username = deepcopy(user.user_id), deepcopy(user.username)
        expire = datetime.utcnow() + self.access_expiration_time
        token_dict = {
            "user_id": user_id,
        }
        token_db = AccessTokenDB(**token_dict, date_expires=expire)
        db.add(token_db)
        await db.flush()
        to_encode = {"sub": username, "id": token_db.token_id}
        encoded_jwt_access = jwt.encode(to_encode, self.jwt_access_secret, algorithm=self.algorithm)
        token_db.access_token = encoded_jwt_access
        await db.commit()
        return encoded_jwt_access

    async def create_refresh_token(self, db: AsyncSession, user: UserModel):
        await delete_by_model_value(db, RefreshTokenDB, RefreshTokenDB.user_id, user.user_id)
        await db.commit()
        user_id, username = deepcopy(user.user_id), deepcopy(user.username)
        expire = datetime.utcnow() + self.refresh_expiration_time
        token_dict = {
            "user_id": user_id
        }
        token_db = RefreshTokenDB(**token_dict, date_expires=expire)
        db.add(token_db)
        await db.flush()
        to_encode = {"sub": username, "id": token_db.token_id}
        encoded_jwt_access = jwt.encode(to_encode, self.jwt_refresh_secret, algorithm=self.algorithm)
        token_db.refresh_token = encoded_jwt_access
        await db.commit()
        return encoded_jwt_access

    async def authenticate_user(self, db: AsyncSession, token: str, plain_password: str) -> UserDB:
        """

        :raises USER_NOT_EXISTS_EXCEPTION:
        :raises NOT_VALID_CREDENTIALS_EXCEPTION:
        :raises USER_PASSWORD_INVALID_EXCEPTION:
        :raises TOKEN_EXPIRED_EXCEPTION:
        """
        try:
            payload = jwt.decode(token, self.jwt_access_secret, algorithms=[self.algorithm])
        except JWTError:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        token_db = await get_by_model_value(db, AccessTokenDB, AccessTokenDB.token_id, payload.get("id"))
        if not token_db:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        elif token_db.date_expires < pytz.UTC.localize(datetime.utcnow()):
            await delete_by_model_value(db, AccessTokenDB, AccessTokenDB.token_id, token_db.token_id)
            await db.commit()
            raise TOKEN_EXPIRED_EXCEPTION
        user_db = await get_by_model_value(db, UserDB, UserDB.user_id, token_db.user_id)
        if not user_db:
            raise USER_NOT_EXISTS_EXCEPTION
        if not await self.password_hasher.verify_password(plain_password, user_db.hashed_password):
            raise USER_PASSWORD_INVALID_EXCEPTION
        return user_db
