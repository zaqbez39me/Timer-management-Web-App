from fastapi_app.api.exceptions.token import (NOT_VALID_CREDENTIALS_EXCEPTION,
                                              TOKEN_EXPIRED_EXCEPTION,
                                              USER_NOT_EXISTS_EXCEPTION)

user_not_exists = USER_NOT_EXISTS_EXCEPTION.__dict__()

not_valid_credentials = NOT_VALID_CREDENTIALS_EXCEPTION.__dict__()

token_expired = TOKEN_EXPIRED_EXCEPTION.__dict__()
