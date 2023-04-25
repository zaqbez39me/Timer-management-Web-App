from datetime import datetime

from sqlalchemy import Column, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR

from fastapi_app.database.models import Base


class TimerDB(Base):
    __tablename__ = 'timer'
    timer_name = Column("timer_name", VARCHAR(30), primary_key=True)
    user_id = Column(BIGINT, ForeignKey('user.user_id'), primary_key=True)
    start_datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    duration_seconds = Column(BIGINT, nullable=False)
