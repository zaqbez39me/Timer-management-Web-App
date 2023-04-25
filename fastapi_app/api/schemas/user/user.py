from datetime import datetime

from pydantic import BaseModel, constr


class UserModel(BaseModel):
    user_id: int
    username: constr(min_length=1, max_length=20)
    date_joined: datetime

