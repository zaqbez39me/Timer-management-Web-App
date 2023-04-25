from typing import Type

from pydantic import BaseModel

from fastapi_app.database.models import Base


def db_model_to_schema(db_obj: Base, model: Type[BaseModel]) -> BaseModel:
    fields = {field.name: getattr(db_obj, field.name) for field in db_obj.__table__.columns}
    return model(**fields)
