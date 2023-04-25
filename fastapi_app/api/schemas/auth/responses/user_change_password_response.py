from pydantic import BaseModel

from fastapi_app.api.schemas.user import UserModel


class UserChangePasswordResponse(BaseModel):
    user: UserModel
    message: str
