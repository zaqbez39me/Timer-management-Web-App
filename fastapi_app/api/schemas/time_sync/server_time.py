from datetime import datetime

from pydantic import BaseModel


class ServerTimeResponse(BaseModel):
    server_time: datetime
