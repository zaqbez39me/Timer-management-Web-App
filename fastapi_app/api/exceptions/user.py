from fastapi import HTTPException
from starlette import status

USER_PASSWORD_INVALID_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User password is invalid!",
    headers={"WWW-Authenticate": "Bearer", "X-Error-Type": "User-Password-Is-Invalid"},
)

USER_CREDENTIALS_ARE_INVALID_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
    headers={"WWW-Authenticate": "Bearer", "X-Error-Type": "User-Password-Or-Username-Invalid"},
)

USER_USERNAME_OCCUPIED_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already in use.",
    headers={"WWW-Authenticate": "Bearer", "X-Error-Type": "Username-Occupied"},
)