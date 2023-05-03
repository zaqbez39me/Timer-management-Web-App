from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from fastapi_app.database.models import Base
from fastapi_app.database.models.token.token import Token


class RefreshTokenDB(Token, Base):
    __tablename__ = "refresh_token"
    refresh_token = Column(String, nullable=True)
    session = relationship("SessionDB", back_populates="refresh_token")
