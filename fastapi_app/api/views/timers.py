from typing import Annotated

from fastapi import APIRouter, Depends, Cookie, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_app.api import oauth2_scheme
from fastapi_app.api.exceptions.token import NOT_VALID_CREDENTIALS_EXCEPTION
from fastapi_app.api.schemas.timers.timer import Timer
from fastapi_app.api.schemas.timers.timer_rename_request import TimerRenameRequest
from fastapi_app.api.schemas.timers.timer_request import TimerRequest
from fastapi_app.api.utils.session import session_validate
from fastapi_app.api.utils.session.session_to_user_id import session_to_user_id
from fastapi_app.api.utils.token import verify_access_token
from fastapi_app.database import db_engine
from fastapi_app.custom_database.utils import CustomDBWorker, get_custom_db_worker

timers_router = APIRouter(tags=["timers"], prefix="/timers")


@timers_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED
)
async def add_timer(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        new_timer: Timer,
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
        worker: CustomDBWorker = Depends(get_custom_db_worker(CustomDBWorker))
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, access_token, session_id)
    user_id = await session_to_user_id(db, token_data.session_id)
    return await worker.add_timer_for_user(user_id=user_id,
                                           name=new_timer.name,
                                           start_time=new_timer.start_time,
                                           duration_seconds=new_timer.duration_seconds,
                                           active=new_timer.active)


@timers_router.post(
    "/resume",
    status_code=status.HTTP_200_OK
)
async def resume_timer(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        timer_request: TimerRequest,
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
        worker: CustomDBWorker = Depends(get_custom_db_worker(CustomDBWorker))
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, access_token, session_id)
    user_id = await session_to_user_id(db, token_data.session_id)
    resp = await worker.resume_timer(user_id, timer_request.name)
    return resp


@timers_router.post(
    "/stop",
    status_code=status.HTTP_200_OK
)
async def stop_timer(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        timer_request: TimerRequest,
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
        worker: CustomDBWorker = Depends(get_custom_db_worker(CustomDBWorker))
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, access_token, session_id)
    user_id = await session_to_user_id(db, token_data.session_id)
    resp = await worker.stop_timer(user_id, timer_request.name)
    return resp


@timers_router.post(
    "/reset",
    status_code=status.HTTP_200_OK
)
async def reset_timer(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        timer_request: TimerRequest,
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
        worker: CustomDBWorker = Depends(get_custom_db_worker(CustomDBWorker))
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, access_token, session_id)
    user_id = await session_to_user_id(db, token_data.session_id)
    resp = await worker.reset_timer(user_id, timer_request.name)
    return resp


@timers_router.post(
    "/change-timer-duration",
    status_code=status.HTTP_200_OK
)
async def change_timer_duration(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        name: Annotated[str, Body(alias="name")],
        timer_duration: Annotated[int, Body(alias="timer_duration")],
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
        worker: CustomDBWorker = Depends(get_custom_db_worker(CustomDBWorker))
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, access_token, session_id)
    user_id = await session_to_user_id(db, token_data.session_id)
    resp = await worker.change_timer_duration(user_id, name, timer_duration)
    return resp


@timers_router.delete(
    "/remove",
    status_code=status.HTTP_200_OK
)
async def remove_timer(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        timer_request: TimerRequest,
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
        worker: CustomDBWorker = Depends(get_custom_db_worker(CustomDBWorker))
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, access_token, session_id)
    user_id = await session_to_user_id(db, token_data.session_id)
    resp = await worker.remove_timer_for_user(user_id, timer_request.name)
    return resp


@timers_router.post(
    "/rename",
    status_code=status.HTTP_200_OK
)
async def rename_timer(
        access_token: Annotated[str, Depends(oauth2_scheme)],
        timer_request: TimerRenameRequest,
        db: AsyncSession = Depends(db_engine.session),
        session_id: str | None = Cookie(default=None),
        worker: CustomDBWorker = Depends(get_custom_db_worker(CustomDBWorker))
):
    if not session_id or not await session_validate(db, session_id):
        raise NOT_VALID_CREDENTIALS_EXCEPTION
    token_data = await verify_access_token(db, access_token, session_id)
    user_id = await session_to_user_id(db, token_data.session_id)
    resp = await worker.rename_timer_for_user(
        user_id,
        timer_request.name,
        timer_request.new_name
    )
    return resp
