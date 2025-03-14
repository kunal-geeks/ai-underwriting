import enum


class StatusCode(enum.IntEnum):
    """
    Enum for HTTP status codes to improve readability and maintainability.
    """
    SUCCESS = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500