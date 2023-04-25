from fastapi_app.api import settings
from fastapi_app.database.engine import DatabaseEngine

db_engine = DatabaseEngine(settings.database_url)
