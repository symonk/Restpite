from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple

from ..http.authentication import Auth
from ..http.authentication import NoAuth


class Configuration:
    def __init__(
        self,
        headers: Optional[Mapping[str, str]] = None,
        base_url: Optional[str] = None,
        auth: Optional[Auth] = None,
        ok_response_codes: Optional[Iterable[int]] = None,
        retry: Optional[Tuple[int, Exception]] = None,
        hooks: Optional[List[Callable[[Any, Any], Any]]] = None,
        timeouts: Optional[Tuple[int, int]] = None,
        default_query_strings: Optional[Mapping[str, str]] = None,
        default_cookies: Optional[Mapping[str, str]] = None,
    ):
        self.headers = headers or {}
        self.base_url = base_url
        self.auth = auth or NoAuth()
        self.ok_response_codes = ok_response_codes
        self.retry = retry or ()
        self.hooks = hooks or []
        self.timeouts = timeouts or (30, 15)
        self.default_query_strings = default_query_strings or {}
        self.default_cookies = default_cookies or {}
