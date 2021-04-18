from typing import Any
from typing import Mapping

from httpx import _types  # noqa

# Request related types
HTTP_URLTYPES_ALIAS = _types.URLTypes
HTTP_CONTENT_ALIAS = _types.RequestContent
HTTP_DATA_ALIAS = Mapping[Any, Any]
HTTP_FILES_ALIAS = _types.RequestFiles
HTTP_JSON_ALIAS = Any
HTTP_QUERY_STRING_ALIAS = _types.QueryParamTypes
HTTP_HEADERS_ALIAS = _types.HeaderTypes
HTTP_COOKIES_ALIAS = _types.CookieTypes
HTTP_AUTH_ALIAS = _types.AuthTypes
HTTP_TIMEOUT_ALIAS = _types.TimeoutTypes

HTTP_VERIFY_ALIAS = _types.VerifyTypes
