from datetime import timedelta

from pydantic import BaseSettings, Field

# Hashing settings
PASSWORD_SCHEMES = ["bcrypt"]

TOKEN_URL = "auth/login"
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_DELTA = timedelta(minutes=15)
REFRESH_TOKEN_DELTA = timedelta(days=3)


# Postgres Settings
class PostgresSettings(BaseSettings):
    pg_username: str = Field(default="postgres", env="PG_USERNAME")
    pg_password: str = Field(default="password", env="PG_PASSWORD")
    pg_ip: str = Field(default="pg", env="PG_IP")
    pg_name: str = Field(default="postgres", env="PG_NAME")
    pg_port: int | str = Field(5432, env="PG_PORT")

    class Config:
        env_prefix = "PG_"
        env_file_encoding = "utf-8"

    @property
    def pg_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.pg_username}:{self.pg_password}"
            f"@{self.pg_ip}:{self.pg_port}/{self.pg_name}"
        )


class RedisSettings(BaseSettings):
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")

    class Config:
        env_prefix = "REDIS_"
        env_file_encoding = "utf-8"


# Secrets settings
class SecretSettings(BaseSettings):
    access_secret_key: str = Field(..., env="SECRET_ACCESS_KEY")
    refresh_secret_key: str = Field(..., env="SECRET_REFRESH_KEY")
    redis_secret: str = Field(..., env="SECRET_REDIS")

    class Config:
        env_prefix = "SECRET_"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    password_schemes: list[str] = PASSWORD_SCHEMES
    token_url: str = TOKEN_URL
    token_algorithm: str = TOKEN_ALGORITHM
    access_token_delta: timedelta = ACCESS_TOKEN_DELTA
    refresh_token_delta: timedelta = REFRESH_TOKEN_DELTA


redis_settings = RedisSettings()
secret_settings = SecretSettings()
pg_settings = PostgresSettings()
settings = Settings()
