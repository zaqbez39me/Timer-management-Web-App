from fastapi_app.api.exceptions import BaseHTTPError, not_valid_credentials
from fastapi_app.api.exceptions.dicts.token import token_expired, user_not_exists


class TokenError401(BaseHTTPError):
    description = "Error with credentials. Not valid token."
    examples = [token_expired, not_valid_credentials, user_not_exists]
