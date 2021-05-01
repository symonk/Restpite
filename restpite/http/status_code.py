from __future__ import annotations

from typing import NamedTuple


class StatusCode(NamedTuple):
    code: int
    message: str

    def __eq__(self, other: object) -> bool:
        """
        Custom status code objects are considered equal if their `code` integers are equal
        """
        return self.code == getattr(other, "code", other)  # type: ignore

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)  # type: ignore

    @classmethod
    def from_code(cls, code: int) -> StatusCode:
        status_code = CODES_MAP.get(code)
        if status_code is None:
            raise ValueError(f"Response status code: {code} is non-existent!")
        return status_code

    def __repr__(self) -> str:
        return f"Response Code: <{self.code}, {self.message}>"


# Informative Status Code Objects
CONTINUE = StatusCode(100, "Continue")
SWITCHING_PROTOCOLS = StatusCode(101, "Switching Protocols")
PROCESSING = StatusCode(102, "Processing")
EARLY_HINTS = StatusCode(103, "Early Hints")

# Successful status codes
OK = StatusCode(200, "OK")
CREATED = StatusCode(201, "Created")
ACCEPTED = StatusCode(202, "OK")
NON_AUTHORITATIVE_INFORMATION = StatusCode(203, "Non-Authoritative Information")
NO_CONTENT = StatusCode(204, "No Content")
RESET_CONTENT = StatusCode(205, "Reset Content")
PARTIAL_CONTENT = StatusCode(206, "Partial Content")
MULTI_STATUS = StatusCode(207, "Multi-Status")
ALREADY_REPORTED = StatusCode(208, "Already Reported")
IM_USED = StatusCode(226, "IM Used")

# Redirection status codes
MULTIPLE_CHOICES = StatusCode(300, "Multiple Choices")
MOVED_PERMANENTLY = StatusCode(301, "Moved Permanently")
FOUND = StatusCode(302, "Found")
SEE_OTHER = StatusCode(303, "See Other")
NOT_MODIFIED = StatusCode(304, "Not Modified")
USE_PROXY = StatusCode(305, "Use Proxy")
TEMPORARY_REDIRECT = StatusCode(307, "Temporary Redirect")
PERMANENT_REDIRECT = StatusCode(308, "Permanent Redirect")

# Client Error status codes
BAD_REQUEST = StatusCode(400, "Bad Request")
UNAUTHORIZED = StatusCode(401, "Unauthorized")
PAYMENT_REQUIRED = StatusCode(402, "Payment Required")
FORBIDDEN = StatusCode(403, "Forbidden")
NOT_FOUND = StatusCode(404, "Not Found")
METHOD_NOT_ALLOWED = StatusCode(405, "Method Not Allowed")
NOT_ACCEPTABLE = StatusCode(406, "Not Acceptable")
PROXY_AUTHENTICATION_REQUIRED = StatusCode(407, "Proxy Authentication Required")
REQUEST_TIMEOUT = StatusCode(408, "Request Timeout")
CONFLICT = StatusCode(409, "Conflict")
GONE = StatusCode(410, "Gone")
LENGTH_REQUIRED = StatusCode(411, "Length Required")
PRECONDITION_FAILED = StatusCode(412, "Precondition Failed")
REQUEST_ENTITY_TOO_LARGE = StatusCode(413, "Request Entity Too Large")
REQUEST_URI_TOO_LONG = StatusCode(414, "Request-URI Too Long")
UNSUPPORTED_MEDIA_TYPE = StatusCode(415, "Unsupported Media Type")
REQUESTED_RANGE_NOT_SATISFIABLE = StatusCode(416, "Requested Range Not Satisfiable")
EXPECTATION_FAILED = StatusCode(417, "Expectation Failed")
IM_A_TEAPOT = StatusCode(418, "I'm a teapot")
MISDIRECTED_REQUEST = StatusCode(421, "Misdirected Request")
UNPROCESSABLE_ENTITY = StatusCode(422, "Unprocessable Entity")
LOCKED = StatusCode(423, "Locked")
FAILED_DEPENDENCY = StatusCode(424, "Failed Dependency")
TOO_EARLY = StatusCode(425, "Too Early")
UPGRADE_REQUIRED = StatusCode(426, "Upgrade Required")
PRECONDITION_REQUIRED = StatusCode(428, "Precondition Required")
TOO_MANY_REQUESTS = StatusCode(429, "Too Many Requests")
REQUEST_HEADER_FIELDS_TOO_LARGE = StatusCode(431, "Request Header Fields Too Large")
UNAVAILABLE_FOR_LEGAL_REASONS = StatusCode(451, "Unavailable For Legal Reasons")

# Server Error status codes
INTERNAL_SERVER_ERROR = StatusCode(500, "Internal Server Error")
NOT_IMPLEMENTED = StatusCode(501, "Not Implemented")
BAD_GATEWAY = StatusCode(502, "Bad Gateway")
SERVICE_UNAVAILABLE = StatusCode(503, "Service Unavailable")
GATEWAY_TIMEOUT = StatusCode(504, "Gateway Timeout")
HTTP_VERSION_NOT_SUPPORTED = StatusCode(505, "HTTP Version Not Supported")
VARIANT_ALSO_NEGOTIATES = StatusCode(506, "Variant Also Negotiates")
INSUFFICIENT_STORAGE = StatusCode(507, "Insufficient Storage")
LOOP_DETECTED = StatusCode(508, "Loop Detected")
NOT_EXTENDED = StatusCode(510, "Not Extended")
NETWORK_AUTHENTICATION_REQUIRED = StatusCode(511, "Network Authentication Required")

CODES_MAP = {
    100: CONTINUE,
    101: SWITCHING_PROTOCOLS,
    102: PROCESSING,
    103: EARLY_HINTS,
    200: OK,
    201: CREATED,
    202: ACCEPTED,
    203: NON_AUTHORITATIVE_INFORMATION,
    204: NO_CONTENT,
    205: RESET_CONTENT,
    206: PARTIAL_CONTENT,
    207: MULTI_STATUS,
    208: ALREADY_REPORTED,
    226: IM_USED,
    300: MULTIPLE_CHOICES,
    301: MOVED_PERMANENTLY,
    302: FOUND,
    303: SEE_OTHER,
    304: NOT_MODIFIED,
    305: USE_PROXY,
    307: TEMPORARY_REDIRECT,
    308: PERMANENT_REDIRECT,
    400: BAD_REQUEST,
    401: UNAUTHORIZED,
    402: PAYMENT_REQUIRED,
    403: FORBIDDEN,
    404: NOT_FOUND,
    405: METHOD_NOT_ALLOWED,
    406: NOT_ACCEPTABLE,
    407: PROXY_AUTHENTICATION_REQUIRED,
    408: REQUEST_TIMEOUT,
    409: CONFLICT,
    410: GONE,
    411: LENGTH_REQUIRED,
    412: PRECONDITION_FAILED,
    413: REQUEST_ENTITY_TOO_LARGE,
    414: REQUEST_URI_TOO_LONG,
    415: UNSUPPORTED_MEDIA_TYPE,
    416: REQUESTED_RANGE_NOT_SATISFIABLE,
    417: EXPECTATION_FAILED,
    418: IM_A_TEAPOT,
    421: MISDIRECTED_REQUEST,
    422: UNPROCESSABLE_ENTITY,
    423: LOCKED,
    424: FAILED_DEPENDENCY,
    425: TOO_EARLY,
    426: UPGRADE_REQUIRED,
    428: PRECONDITION_REQUIRED,
    429: TOO_MANY_REQUESTS,
    431: REQUEST_HEADER_FIELDS_TOO_LARGE,
    451: UNAVAILABLE_FOR_LEGAL_REASONS,
    500: INTERNAL_SERVER_ERROR,
    501: NOT_IMPLEMENTED,
    502: BAD_GATEWAY,
    503: SERVICE_UNAVAILABLE,
    504: GATEWAY_TIMEOUT,
    505: HTTP_VERSION_NOT_SUPPORTED,
    506: VARIANT_ALSO_NEGOTIATES,
    507: INSUFFICIENT_STORAGE,
    508: LOOP_DETECTED,
    510: NOT_EXTENDED,
    511: NETWORK_AUTHENTICATION_REQUIRED,
}
