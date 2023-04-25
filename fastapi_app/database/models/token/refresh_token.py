from datetime import datetime

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from fastapi_app.database.models import Base
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP


class RefreshTokenDB(Base):
    __tablename__ = "refresh_token"
    token_id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("user.user_id", ondelete="CASCADE"), unique=True, index=True)
    refresh_token = Column(String, nullable=True)
    date_expires = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    user = relationship("UserDB", back_populates="refresh_token")
