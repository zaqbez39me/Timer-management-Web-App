from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.api.settings import settings
from fastapi_app.api.utils.auth.password_hashing import PasswordHasher
from fastapi_app.database.models.user import UserDB
from fastapi_app.database.utils import get_by_model_value


class UserAuthenticator:
    def __init__(self):
        self.password_hasher = PasswordHasher(settings.password_schemes)

    async def register_new_user(self, db: AsyncSession, username: str, password: str):
        user = UserDB(
            username=username,
            hashed_password=await self.password_hasher.get_password_hash(password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def authenticate_user(self, db: AsyncSession, username: str, password: str):
        user: UserDB = await get_by_model_value(db, UserDB, UserDB.username, username)
        if not user:
            return False
        if not await self.password_hasher.verify_password(
            password, user.hashed_password
        ):
            return False
        return user
