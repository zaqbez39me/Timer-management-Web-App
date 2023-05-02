from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR
from sqlalchemy.orm import relationship

from fastapi_app.database.models import Base


class RefreshTokenDB(Base):
    __tablename__ = "refresh_token"
    token_id = Column(BIGINT, primary_key=True, index=True)
    session_id = Column(
        VARCHAR(40),
        ForeignKey("session.session_id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    refresh_token = Column(String, nullable=True)
    session = relationship("SessionDB", back_populates="refresh_token")
