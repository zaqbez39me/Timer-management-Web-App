from sqlalchemy.orm import declarative_base

Base = declarative_base()

from fastapi_app.database.models.timer import TimerDB
