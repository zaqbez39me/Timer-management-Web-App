user_password_invalid = {
    "summary": "User password is invalid!",
    "value": {
        "headers": {"WWW-Authenticate": "Bearer", "X-Error-Type": "User-Password-Is-Invalid"}
    },

}

user_credentials_invalid = {
    "summary": "Incorrect username or password",
    "value": {
        "headers": {"WWW-Authenticate": "Bearer", "X-Error-Type": "User-Password-Or-Username-Invalid"}
    },
}

user_username_occupied = {
    "summary": "Username already occupied.",
    "value": {
        "headers": {"WWW-Authenticate": "Bearer", "X-Error-Type": "Username-Occupied"}
    },
}
