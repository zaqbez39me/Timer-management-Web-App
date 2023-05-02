from fastapi_app.api.exceptions import BaseHTTPError
from fastapi_app.api.exceptions.dicts.user import user_username_occupied


class UserRegisterError409(BaseHTTPError):
    description = "Error with username. Username already occupied!"
    examples = [user_username_occupied]
