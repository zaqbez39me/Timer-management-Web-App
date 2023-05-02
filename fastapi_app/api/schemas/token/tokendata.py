from datetime import datetime

from pydantic import BaseModel


class TokenData(BaseModel):
    token_id: int
    session_id: str | None = None
    token: str
    datetime_expires: datetime
    token_type: str
