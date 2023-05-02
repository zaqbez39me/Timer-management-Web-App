from starlette import status

from fastapi_app.api.exceptions.base import BaseHTTPException

USER_NOT_EXISTS_EXCEPTION = BaseHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User does not exist!",
    x_error_type="User-Not-Exists",
)

NOT_VALID_CREDENTIALS_EXCEPTION = BaseHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate token credentials.",
    x_error_type="Invalid-Credentials",
)

TOKEN_EXPIRED_EXCEPTION = BaseHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired.",
    x_error_type="Token-Expired",
)
