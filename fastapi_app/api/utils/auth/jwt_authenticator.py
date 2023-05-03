from datetime import datetime

import pytz
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.api import settings
from fastapi_app.api.exceptions.token import (NOT_VALID_CREDENTIALS_EXCEPTION,
                                              TOKEN_EXPIRED_EXCEPTION,
                                              USER_NOT_EXISTS_EXCEPTION)
from fastapi_app.api.exceptions.user import USER_PASSWORD_INVALID_EXCEPTION
from fastapi_app.api.schemas.token import TokenData
from fastapi_app.api.schemas.token.blacklist_token import TokenBlacklist
from fastapi_app.api.utils.auth.password_hashing import PasswordHasher
from fastapi_app.cache import redis_client
from fastapi_app.database.models import Base
from fastapi_app.database.models.token import AccessTokenDB, RefreshTokenDB
from fastapi_app.database.models.user import SessionDB, UserDB
from fastapi_app.database.utils import (delete_by_model_value,
                                        get_by_model_value)


class JWTAuthenticator:
    def __init__(
        self,
        access_secret_key: str,
        refresh_secret_key: str,
        algorithm,
        access_expiration_time,
        refresh_expiration_time,
    ):
        self.password_hasher = PasswordHasher(settings.password_schemes)
        self.jwt_access_secret: str = access_secret_key
        self.jwt_refresh_secret: str = refresh_secret_key
        self.algorithm = algorithm
        self.access_expiration_time = access_expiration_time
        self.refresh_expiration_time = refresh_expiration_time

    async def create_tokens(self, db: AsyncSession, session_id: str) -> dict:
        encoded_jwt_access = await self.create_access_token(
            db=db, session_id=session_id
        )
        encoded_jwt_refresh = await self.create_refresh_token(
            db=db, session_id=session_id
        )
        return {
            "access_token": encoded_jwt_access,
            "refresh_token": encoded_jwt_refresh,
        }

    async def get_access_token_data(
        self, db: AsyncSession, token: str, session_id: str
    ) -> TokenData | bool:
        return await self.__get_token_data(
            db, AccessTokenDB, token, session_id, self.jwt_access_secret
        )

    async def get_refresh_token_data(
        self, db: AsyncSession, token: str, session_id: str
    ) -> TokenData | bool:
        return await self.__get_token_data(
            db, RefreshTokenDB, token, session_id, self.jwt_refresh_secret
        )

    async def __get_token_data(
        self, db: AsyncSession, db_model: Base, token: str, session_id: str, secret: str
    ) -> TokenData | bool:
        """
        :raises NOT_VALID_CREDENTIALS_EXCEPTION:
        """
        if await self.__is_blacklisted(token):
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        try:
            payload = jwt.decode(token, secret, algorithms=[self.algorithm])
            if payload.get("session_id") != session_id:
                raise NOT_VALID_CREDENTIALS_EXCEPTION
            session_id: int = payload.get("session_id")
            if session_id:
                token_db = await get_by_model_value(
                    db, db_model, db_model.token_id, payload.get("id")
                )
                if token_db:
                    token_data = TokenData(
                        token_id=token_db.token_id,
                        session_id=session_id,
                        token=token,
                        datetime_expires=payload.get("date_expires"),
                        token_type="bearer",
                    )
                    return token_data
        except JWTError:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        raise NOT_VALID_CREDENTIALS_EXCEPTION

    async def get_access_token_data_no_validation(self, token):
        return await self.__get_token_data_no_validation(token, self.jwt_access_secret)

    async def get_refresh_token_data_no_validation(self, token):
        return await self.__get_token_data_no_validation(token, self.jwt_refresh_secret)

    async def __get_token_data_no_validation(self, token, secret):
        payload = jwt.decode(token, secret, algorithms=[self.algorithm])
        format_str = "%Y-%m-%d %H:%M:%S.%f"
        date_expires = pytz.UTC.localize(
            dt=datetime.strptime(payload.get("date_expires"), format_str)
        )
        return TokenData(
            token_id=payload.get("id"),
            user_id=payload.get("user_id"),
            token=token,
            datetime_expires=date_expires,
            token_type="bearer",
        )

    async def create_access_token(self, db: AsyncSession, session_id: str):
        await delete_by_model_value(
            db, AccessTokenDB, AccessTokenDB.session_id, session_id
        )
        await db.commit()
        expire = datetime.utcnow() + self.access_expiration_time
        token_db = AccessTokenDB(session_id=session_id)
        db.add(token_db)
        await db.flush()
        to_encode = {
            "session_id": session_id,
            "date_expires": str(expire),
            "id": token_db.token_id,
        }
        encoded_jwt_access = jwt.encode(
            to_encode, self.jwt_access_secret, algorithm=self.algorithm
        )
        token_db.access_token = encoded_jwt_access
        await db.commit()
        return encoded_jwt_access

    async def create_refresh_token(self, db: AsyncSession, session_id: str):
        await delete_by_model_value(
            db, RefreshTokenDB, RefreshTokenDB.session_id, session_id
        )
        await db.commit()
        expire = datetime.utcnow() + self.refresh_expiration_time
        token_db = RefreshTokenDB(session_id=session_id)
        db.add(token_db)
        await db.flush()
        to_encode = {
            "session_id": session_id,
            "date_expires": str(expire),
            "id": token_db.token_id,
        }
        encoded_jwt_access = jwt.encode(
            to_encode, self.jwt_refresh_secret, algorithm=self.algorithm
        )
        token_db.refresh_token = encoded_jwt_access
        await db.commit()
        return encoded_jwt_access

    @staticmethod
    async def add_to_blacklist(token, user_id, expiration):
        await redis_client.set_async(
            name=f"blacklist:{token}",
            value=TokenBlacklist(user_id=user_id),
            expiration=expiration,
        )

    @staticmethod
    async def __is_blacklisted(token):
        if await redis_client.get_async(f"blacklist:{token}", model=TokenBlacklist):
            return True
        return False

    async def authenticate_user(
        self, db: AsyncSession, token: str, plain_password: str, session_id: str
    ) -> UserDB:
        """
        :raises USER_NOT_EXISTS_EXCEPTION:
        :raises NOT_VALID_CREDENTIALS_EXCEPTION:
        :raises USER_PASSWORD_INVALID_EXCEPTION:
        :raises TOKEN_EXPIRED_EXCEPTION:
        """
        if await self.__is_blacklisted(token):
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        try:
            payload = jwt.decode(
                token, self.jwt_access_secret, algorithms=[self.algorithm]
            )
            if payload.get("session_id") != session_id:
                raise NOT_VALID_CREDENTIALS_EXCEPTION
            format_str = "%Y-%m-%d %H:%M:%S.%f"
            date_expires = pytz.UTC.localize(
                dt=datetime.strptime(payload.get("date_expires"), format_str)
            )
            if date_expires < pytz.UTC.localize(dt=datetime.utcnow()):
                await delete_by_model_value(
                    db, AccessTokenDB, AccessTokenDB.token_id, payload.get("id")
                )
                await db.commit()
                raise TOKEN_EXPIRED_EXCEPTION
        except JWTError:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        token_db = await get_by_model_value(
            db, AccessTokenDB, AccessTokenDB.token_id, payload.get("id")
        )
        if not token_db:
            raise NOT_VALID_CREDENTIALS_EXCEPTION
        session = await get_by_model_value(
            db, SessionDB, SessionDB.session_id, payload.get("session_id")
        )
        user_db = await get_by_model_value(db, UserDB, UserDB.user_id, session.user_id)
        if not user_db:
            raise USER_NOT_EXISTS_EXCEPTION
        if not await self.password_hasher.verify_password(
            plain_password, user_db.hashed_password
        ):
            raise USER_PASSWORD_INVALID_EXCEPTION
        return user_db
