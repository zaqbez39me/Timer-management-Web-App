from fastapi import FastAPI

from fastapi_app.api.views import auth, time_sync, timers, token
from fastapi_app.database import db_engine
from fastapi_app.database.models import Base


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
    engine = await db_engine.get_engine()
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await db_engine.finalize()
