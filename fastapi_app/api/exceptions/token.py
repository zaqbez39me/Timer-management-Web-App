from fastapi import HTTPException
from starlette import status

USER_NOT_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User does not exist!",
    headers={"WWW-Authenticate": "Bearer", "X-Error-Type": "User-Not-Exists"},
)

NOT_VALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate token credentials.",
    headers={"WWW-Authenticate": "Bearer", "X-Error-Type": "Invalid-Credentials"},
)

TOKEN_EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired.",
    headers={"WWW-Authenticate": "Bearer", "X-Error-Type": "Token-Expired"},
)