from datetime import datetime
from typing import Annotated

from fastapi import Body
from pydantic import BaseModel


class Timer(BaseModel):
    name: Annotated[str, Body(alias='name')]
    start_time: Annotated[datetime, Body(alias='start_time')] = datetime.utcnow()
    duration_seconds: Annotated[int, Body(alias='duration_seconds')]
    active: Annotated[bool, Body(alias='active')] = False
