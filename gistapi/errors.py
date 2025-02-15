from typing import Any

import marshmallow
from flask import jsonify


class RequestError(Exception):
    """
    User exceptions wrapper
    """

    def __init__(
        self,
        title: str,
        status_code: int,
        payload: str | list[Any] | dict[Any, Any] | None = None,
    ):
        super(RequestError, self).__init__()
        self.title = title
        self.status_code = status_code
        self.payload = payload

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "code": self.status_code,
            "error": self.title,
            "message": self.payload,
        }


def error_wrapper(exception: RequestError):
    response = jsonify(exception.to_dict())
    return response, exception.status_code


def request_validation_error(exception: marshmallow.ValidationError):
    exc = RequestError(
        "Request validation errors", status_code=400, payload=exception.messages
    )
    return error_wrapper(exc)


def generic_error(exception: BaseException):
    exc = RequestError("Server error", status_code=500, payload=str(exception))
    return error_wrapper(exc)
