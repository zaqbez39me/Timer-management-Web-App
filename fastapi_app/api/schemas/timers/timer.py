from datetime import datetime
from typing import Annotated

from fastapi import Body
from pydantic import BaseModel
from typing import Optional


class Timer(BaseModel):
    name: Annotated[str, Body(alias='name')]
    start_time: Annotated[Optional[datetime], Body(alias='start_time')]
    duration_seconds: Annotated[int, Body(alias='duration_seconds')]
    active: Annotated[bool, Body(alias='active')] = False
