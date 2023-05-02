from pydantic import BaseModel


class TokenBlacklist(BaseModel):
    user_id: int
