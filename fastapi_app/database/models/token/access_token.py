from datetime import datetime

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from fastapi_app.database.models import Base
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP


class AccessTokenDB(Base):
    __tablename__ = "access_token"
    token_id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("user.user_id", ondelete="CASCADE"), index=True)
    access_token = Column(String, nullable=True)
    date_expires = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    user = relationship("UserDB", back_populates="access_token")
