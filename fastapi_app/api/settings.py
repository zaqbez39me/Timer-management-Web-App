from datetime import timedelta

from pydantic import (
    BaseSettings
)

# Database settings
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"

# Hashing settings
PASSWORD_SCHEMES = ["bcrypt"]

# Token settings
ACCESS_SECRET_KEY: str = "2e2d6d19940a4704db328e58e696849dd04db207bacffa999cb201ae7722bd5a" \
                         "a6ce08219c980e3ee1157807282246952c2fa71e0d193ab7b444cb1eabf25afb"

REFRESH_SECRET_KEY: str = "a6e1d69f01275b89f2b44e835e56517a738b26a43ba3c78877e4237bcf828b4f" \
                          "43a227c61908764e0fe6cc01580f9753caa3a18c110027639920ebe8a7a06039" \
                          "7cae8c2acdf9ae8e0423a387b50effd10a983e166f2108a36fde0b3e66d19b13" \
                          "6ffe4f58ec828d33f1e9a1e9d3ef36b94099a84273406d8d4b1b15a5112c7f88"

TOKEN_URL = "auth/login"
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_DELTA = timedelta(hours=12)
REFRESH_TOKEN_DELTA = timedelta(days=3)


class Settings(BaseSettings):
    database_url: str = DATABASE_URL
    password_schemes: list[str] = PASSWORD_SCHEMES
    access_secret_key: str = ACCESS_SECRET_KEY
    refresh_secret_key: str = REFRESH_SECRET_KEY
    token_url: str = TOKEN_URL
    token_algorithm: str = TOKEN_ALGORITHM
    access_token_delta: timedelta = ACCESS_TOKEN_DELTA
    refresh_token_delta: timedelta = REFRESH_TOKEN_DELTA


settings = Settings()
