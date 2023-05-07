from datetime import timedelta
from typing import Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator

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
    pg_port: str = Field("5432", env="PG_PORT")
    pg_database_uri: Optional[PostgresDsn] = None

    @validator("pg_database_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("pg_username"),
            password=values.get("pg_password"),
            host=values.get("pg_ip"),
            port=values.get("pg_port"),
            path=f"/{values.get('pg_name') or ''}",
        )

    class Config:
        env_prefix = "PG_"
        env_file_encoding = "utf-8"


# Custom-DB can be queried like so:
# requests.get(custom_db_settings.custom_db_url,params={'query':"create entity Meat {mass: int}"} )
class CustomDbSettings(BaseSettings):
    custom_db_ip: str = Field(default="custom_db", env="CUSTOM_DB_IP")
    custom_db_port: str = Field(default="80", env="CUSTOM_DB_PORT")

    class Config:
        env_prefix = "CUSTOM_DB_"
        env_file_encoding = "utf-8"

    @property
    def custom_db_url(self) -> str:
        return (
            f"http://{self.custom_db_ip}:{self.custom_db_port}/Query"
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


custom_db_settings = CustomDbSettings()
redis_settings = RedisSettings()
secret_settings = SecretSettings()
pg_settings = PostgresSettings()

settings = Settings()
