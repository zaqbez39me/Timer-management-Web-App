from typing import Any, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Column, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from fastapi_app.database.models import Base

Model = TypeVar("Model", bound=Base)


def db_model_to_schema(db_obj: Base, model: Type[BaseModel]) -> BaseModel:
    columns = db_obj.__table__.columns
    fields = {field.name: getattr(db_obj, field.name) for field in columns}
    return model(**fields)


async def delete_by_model_value(
    session: AsyncSession,
    model: Type[Model],
    attribute: Column | Any,
    value: Any,
    commit: bool = False,
) -> None:
    await session.execute(delete(model).where(attribute == value))
    if commit:
        await session.commit()


async def get_by_model(
    session: AsyncSession,
    model: Type[Model],
) -> list[Model]:
    res = await session.execute(select(model))
    return res.scalars().all()


async def get_by_model_value(
    session: AsyncSession,
    model: Type[Model],
    attribute: Column | Any,
    value: Any,
    unique: bool = True,
) -> list[Model] | Model:
    res = await session.execute(select(model).where(attribute == value))
    res = res.scalars()
    if unique:
        return res.one_or_none()
    return res.all()


async def add_to_db(session: AsyncSession, item: Base, commit: bool = False):
    session.add(item)
    if commit:
        await session.commit()


async def add_to_db_bg(
    background_tasks: BackgroundTasks,
    session: AsyncSession,
    item: Base,
    commit: bool = False,
):
    background_tasks.add_task(add_to_db, session=session, item=item, commit=commit)


async def delete_by_model_value_bg(
    background_tasks: BackgroundTasks,
    session: AsyncSession,
    model: Type[Model],
    attribute: Column | Any,
    value: Any,
    commit: bool = False,
):
    background_tasks.add_task(
        delete_by_model_value,
        session=session,
        model=model,
        attribute=attribute,
        value=value,
        commit=commit,
    )
