from starlette import status

from fastapi_app.api.exceptions.base import BaseHTTPException

USER_PASSWORD_INVALID_EXCEPTION = BaseHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User password is invalid!",
    x_error_type="User-Password-Is-Invalid",
)

USER_CREDENTIALS_ARE_INVALID_EXCEPTION = BaseHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
    x_error_type="User-Password-Or-Username-Invalid",
)

USER_USERNAME_OCCUPIED_EXCEPTION = BaseHTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already in use.",
    x_error_type="Username-Occupied",
)
