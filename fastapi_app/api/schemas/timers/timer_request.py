from typing import Annotated

from fastapi import Body
from pydantic import BaseModel


class TimerRequest(BaseModel):
    name: Annotated[str, Body(alias='name')]
