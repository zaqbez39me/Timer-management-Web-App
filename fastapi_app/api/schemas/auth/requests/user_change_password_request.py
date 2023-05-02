from fastapi import Query
from pydantic import BaseModel, Field


class UserChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
