from datetime import datetime

import pytz
from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing_extensions import Annotated

from fastapi_app.api import oauth2_scheme
from fastapi_app.api.schemas.time_sync import ServerTimeResponse
from fastapi_app.api.utils.token import verify_access_token
from fastapi_app.database import db_engine

time_sync_router = APIRouter(tags=["time_sync"], prefix="/time_sync")


@time_sync_router.get(
    "", status_code=status.HTTP_200_OK, response_model=ServerTimeResponse
)
async def change_password(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(db_engine.session),
    session_id: str | None = Cookie(default=None),
):
    await verify_access_token(db, access_token, session_id)
    return ServerTimeResponse(server_time=pytz.UTC.localize(dt=datetime.utcnow()))
