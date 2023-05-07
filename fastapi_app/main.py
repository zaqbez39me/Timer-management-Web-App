import time

from fastapi import FastAPI
from starlette.requests import Request

from .api.views import auth, time_sync, timers, token
from .database import db_engine


def get_application() -> FastAPI:
    application = FastAPI(title="TimerManager")
    application.include_router(auth.auth_router)
    application.include_router(time_sync.time_sync_router)
    application.include_router(timers.timers_router)
    application.include_router(token.token_router)
    return application


app = get_application()


@app.on_event("startup")
async def startup():
    """
    This the startup function that
    :return:
    """
    # create db tables
    await db_engine.start()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await db_engine.finalize()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time * 1e3)

    return response
