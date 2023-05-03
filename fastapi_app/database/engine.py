import time
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


class DatabaseEngine:
    def __init__(self, database_url):
        while True:
            self.__engine = create_async_engine(database_url)
            break
        self.__session_maker = async_sessionmaker(
            bind=self.__engine, autocommit=False, class_=AsyncSession, autoflush=False
        )

    async def get_engine(self):
        return self.__engine

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_maker() as session:
            yield session

    async def finalize(self) -> None:
        await self.__engine.dispose()
