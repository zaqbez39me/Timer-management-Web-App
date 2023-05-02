from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR
from sqlalchemy.orm import relationship

from fastapi_app.database.models import Base


class SessionDB(Base):
    __tablename__ = "session"
    session_id = Column("session_id", VARCHAR(40), primary_key=True, index=True)
    user_id = Column(
        "user_id", BIGINT, ForeignKey("user.user_id", ondelete="CASCADE"), index=True
    )
    user = relationship("UserDB")
    access_token = relationship("AccessTokenDB", back_populates="session")
    refresh_token = relationship("RefreshTokenDB", back_populates="session")
