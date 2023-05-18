from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from fastapi_app.database.models import Base


class DatabaseEngine:
    def __init__(self, database_url):
        self.__engine = create_async_engine(database_url)
        self.__session_maker = async_sessionmaker(
            bind=self.__engine, autocommit=False, class_=AsyncSession, autoflush=False
        )

    async def start(self):
        async with self.__engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_maker() as session:
            yield session

    async def finalize(self) -> None:
        await self.__engine.dispose()
