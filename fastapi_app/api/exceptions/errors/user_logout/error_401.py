from fastapi_app.api.exceptions import (BaseHTTPError, not_valid_credentials,
                                        token_expired, user_not_exists)


class UserLogoutError401(BaseHTTPError):
    description = "Error with credentials. Not valid token."
    examples = [not_valid_credentials, user_not_exists, token_expired]
