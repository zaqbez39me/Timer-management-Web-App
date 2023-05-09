from typing import Annotated

from fastapi import Body
from pydantic import BaseModel


class TimerRenameRequest(BaseModel):
    name: Annotated[str, Body(alias='name')]
    new_name: Annotated[str, Body(alias='new_name')]
