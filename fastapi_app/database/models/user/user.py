from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

from fastapi_app.database.models import Base


class UserDB(Base):
    __tablename__ = 'user'
    user_id = Column("user_id", BIGINT, primary_key=True, autoincrement=True, index=True)
    username = Column("username", VARCHAR(20), unique=True, index=True)
    hashed_password = Column("hashed_password", VARCHAR(128))
    date_joined = Column("date_joined", TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    access_token = relationship("AccessTokenDB", back_populates="user")
    refresh_token = relationship("RefreshTokenDB", back_populates="user")
