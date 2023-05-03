from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from fastapi_app.database.models import Base
from fastapi_app.database.models.token.token import Token


class AccessTokenDB(Token, Base):
    __tablename__ = "access_token"
    access_token = Column(String, nullable=True)
    session = relationship("SessionDB", back_populates="access_token")
