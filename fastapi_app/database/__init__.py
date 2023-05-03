"""
Module for database operations
"""

from fastapi_app.api import pg_settings
from fastapi_app.database.engine import DatabaseEngine

db_engine = DatabaseEngine(pg_settings.pg_url)
