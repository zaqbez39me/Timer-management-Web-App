from pydantic import BaseModel


class UserChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
