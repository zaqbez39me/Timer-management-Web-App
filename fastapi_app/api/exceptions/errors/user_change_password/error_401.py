from fastapi_app.api.exceptions import BaseHTTPError
from fastapi_app.api.exceptions.dicts.token import (not_valid_credentials,
                                                    token_expired,
                                                    user_not_exists)
from fastapi_app.api.exceptions.dicts.user import user_password_invalid


class UserChangePasswordError401(BaseHTTPError):
    description = "Wrong credentials."
    examples = [
        not_valid_credentials,
        user_not_exists,
        token_expired,
        user_password_invalid,
    ]
