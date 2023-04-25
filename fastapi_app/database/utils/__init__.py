from typing import TypeVar

from fastapi_app.database.models import Base

Model = TypeVar('Model', bound=Base)

from fastapi_app.database.utils.get_by_model_value import get_by_model_value
from fastapi_app.database.utils.get_by_model import get_by_model
from fastapi_app.database.utils.db_to_schema import db_model_to_schema
from fastapi_app.database.utils.delete_by_model_value import delete_by_model_value
