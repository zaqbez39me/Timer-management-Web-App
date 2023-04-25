from fastapi_app.api.exceptions import BaseHTTPError
from fastapi_app.api.exceptions.dicts.token import not_valid_credentials, user_not_exists, token_expired


class UserMeError401(BaseHTTPError):
    description = "Not valid token or user does not exist."
    examples = [not_valid_credentials, user_not_exists, token_expired]
