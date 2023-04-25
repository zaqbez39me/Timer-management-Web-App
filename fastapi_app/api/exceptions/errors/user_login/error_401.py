from fastapi_app.api.exceptions import BaseHTTPError
from fastapi_app.api.exceptions.dicts.user import user_credentials_invalid


class UserLoginError401(BaseHTTPError):
    description = "Error with credentials. Not valid token."
    examples = [user_credentials_invalid]
