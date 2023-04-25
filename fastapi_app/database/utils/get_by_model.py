from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type

from fastapi_app.database.utils import Model


async def get_by_model(
        session: AsyncSession,
        model: Type[Model],
) -> list[Model]:
    res = await session.execute(select(model))
    return res.scalars().all()
