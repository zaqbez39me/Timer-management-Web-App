from datetime import datetime

from pydantic import BaseModel


class RegistrationResponse(BaseModel):
    user_id: int
    username: str
    date_joined: datetime
    message: str
