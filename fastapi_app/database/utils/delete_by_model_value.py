from sqlalchemy import Column, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, Any

from fastapi_app.database.utils import Model


async def delete_by_model_value(
        session: AsyncSession,
        model: Type[Model],
        attribute: Column | Any,
        value: Any,
        unique: bool = True
) -> None:
    await session.execute(delete(model).where(attribute == value))
