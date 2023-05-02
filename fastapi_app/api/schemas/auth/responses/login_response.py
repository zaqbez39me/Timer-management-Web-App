from pydantic import BaseModel

from fastapi_app.api.schemas.user import UserModel


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    message: str
    data: UserModel
