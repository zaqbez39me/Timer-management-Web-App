from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, status_code, x_error_type, detail=None):
        headers = {"WWW-Authenticate": "Bearer", "X-Error-Type": x_error_type}
        if detail:
            super().__init__(status_code=status_code, detail=detail, headers=headers)
        else:
            super().__init__(
                status_code=status_code, detail="No details.", headers=headers
            )

    def __dict__(self):
        return {"summary": self.detail, "value": {"headers": self.headers}}
