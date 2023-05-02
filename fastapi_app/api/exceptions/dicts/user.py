from fastapi_app.api.exceptions.user import (
    USER_CREDENTIALS_ARE_INVALID_EXCEPTION, USER_PASSWORD_INVALID_EXCEPTION,
    USER_USERNAME_OCCUPIED_EXCEPTION)

user_password_invalid = USER_PASSWORD_INVALID_EXCEPTION.__dict__()

user_credentials_invalid = USER_CREDENTIALS_ARE_INVALID_EXCEPTION.__dict__()

user_username_occupied = USER_USERNAME_OCCUPIED_EXCEPTION.__dict__()
