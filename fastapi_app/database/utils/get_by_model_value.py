from sqlalchemy import Column, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, Any

from fastapi_app.database.utils import Model


async def get_by_model_value(
        session: AsyncSession,
        model: Type[Model],
        attribute: Column | Any,
        value: Any,
        unique: bool = True
) -> list[Model] | Model:
    res = await session.execute(select(model).where(attribute == value))
    res = res.scalars()
    if unique:
        return res.one_or_none()
    return res.all()
