from fastapi.security import OAuth2PasswordBearer

from fastapi_app.api.settings import pg_settings, secret_settings, settings
from fastapi_app.api.utils.auth import (JWTAuthenticator, PasswordHasher,
                                        UserAuthenticator)

password_hasher = PasswordHasher(settings.password_schemes)

jwt_authenticator = JWTAuthenticator(
    access_secret_key=secret_settings.access_secret_key,
    refresh_secret_key=secret_settings.refresh_secret_key,
    algorithm=settings.token_algorithm,
    access_expiration_time=settings.access_token_delta,
    refresh_expiration_time=settings.refresh_token_delta,
)

# Authentication settings
user_authenticator = UserAuthenticator()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.token_url)
