from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR


class Token:
    token_id = Column(BIGINT, primary_key=True, index=True)
    session_id = Column(
        VARCHAR(40),
        ForeignKey("session.session_id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
