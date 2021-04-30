from collections import namedtuple

StatusCode = namedtuple("StatusCode", "code message")

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
INTERNAL_SERVER_ERROR = 500, "Internal Server Error"
NOT_IMPLEMENTED = 501, "Not Implemented"
BAD_GATEWAY = 502, "Bad Gateway"
SERVICE_UNAVAILABLE = 503, "Service Unavailable"
GATEWAY_TIMEOUT = 504, "Gateway Timeout"
HTTP_VERSION_NOT_SUPPORTED = 505, "HTTP Version Not Supported"
VARIANT_ALSO_NEGOTIATES = 506, "Variant Also Negotiates"
INSUFFICIENT_STORAGE = 507, "Insufficient Storage"
LOOP_DETECTED = 508, "Loop Detected"
NOT_EXTENDED = 510, "Not Extended"
NETWORK_AUTHENTICATION_REQUIRED = 511, "Network Authentication Required"
