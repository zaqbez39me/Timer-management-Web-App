from pydantic import BaseModel


class SessionUser(BaseModel):
    user_id: int
