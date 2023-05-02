from fastapi import HTTPException
from pydantic import BaseModel
from typing_extensions import Type

from fastapi_app.api.exceptions.dicts.token import (not_valid_credentials,
                                                    token_expired,
                                                    user_not_exists)


class HTTPError(BaseModel):
    detail: str
    headers: dict

    class Config:
        schema_extra = {
            "example": {
                "detail": "HTTPException raised.",
                "headers": {
                    "WWW-Authenticate": "Bearer",
                    "X-Error-Type": "Error-Type-Text",
                },
            },
        }


class BaseHTTPError(BaseModel):
    description: str
    examples: list


def get_response_schema(error: Type[BaseHTTPError]):
    error = error()
    examples = {}
    for i, item in enumerate(error.examples):
        examples.update({i: item})
    return {
        "description": error.description,
        "content": {"application/json": {"examples": examples}},
    }
