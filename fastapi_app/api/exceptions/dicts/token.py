user_not_exists = {
    "summary": "User does not exist!",
    "value": {
        "headers": {"WWW-Authenticate": "Bearer", "X-Error-Type": "User-Not-Exists"}
    }
}

not_valid_credentials = {
    "summary": "Could not validate token credentials.",
    "value": {
        "headers": {"WWW-Authenticate": "Bearer", "X-Error-Type": "Invalid-Credentials"}
    }
}

token_expired = {
    "summary": "Token expired.",

    "value": {
        "headers": {"WWW-Authenticate": "Bearer", "X-Error-Type": "Token-Expired"}
    }
}
