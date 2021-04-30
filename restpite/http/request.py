from functools import partial
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from restpite import RespiteClient
from restpite import RestpiteResponse
from restpite.http.http_type import HTTP_AUTH_ALIAS
from restpite.http.http_type import HTTP_CONTENT_ALIAS
from restpite.http.http_type import HTTP_COOKIES_ALIAS
from restpite.http.http_type import HTTP_DATA_ALIAS
from restpite.http.http_type import HTTP_FILES_ALIAS
from restpite.http.http_type import HTTP_HEADERS_ALIAS
from restpite.http.http_type import HTTP_JSON_ALIAS
from restpite.http.http_type import HTTP_QUERY_STRING_ALIAS
from restpite.http.http_type import HTTP_TIMEOUT_ALIAS
from restpite.http.http_type import HTTP_URLTYPES_ALIAS
from restpite.http.http_type import HTTP_VERIFY_ALIAS
from restpite.http.verb import DELETE
from restpite.http.verb import GET
from restpite.http.verb import PATCH
from restpite.http.verb import POST
from restpite.http.verb import PUT
from restpite.protocols.restpite_protocols import Notifyable


class RestpiteRequest:
    def __init__(
        self,
        method: str,
        *,
        url: HTTP_URLTYPES_ALIAS,
        content: HTTP_CONTENT_ALIAS = None,
        data: HTTP_DATA_ALIAS = None,
        files: HTTP_FILES_ALIAS = None,
        json: HTTP_JSON_ALIAS = None,
        params: HTTP_QUERY_STRING_ALIAS = None,
        headers: HTTP_HEADERS_ALIAS = None,
        cookies: HTTP_COOKIES_ALIAS = None,
        auth: HTTP_AUTH_ALIAS = None,
        allow_redirects: bool = True,
        timeout: HTTP_TIMEOUT_ALIAS = None,
        retries: int = 0,
        verify: HTTP_VERIFY_ALIAS = False,
        handlers: Optional[List[Notifyable]] = None,
        use_async: bool = False,
        http2: bool = False,
    ) -> None:
        self.method = method
        self.url = url
        self.content = content
        self.data = data
        self.files = files
        self.json = json
        self.params = params
        self.headers = headers
        self.cookies = cookies
        self.auth = auth
        self.allow_redirects = allow_redirects
        self.timeout = timeout
        self.retries = retries
        self.verify = verify
        self.handlers = handlers
        self.adapters = None
        self.use_async = use_async
        self.http2 = http2

    def __call__(self, *args, **kwargs) -> RestpiteResponse:
        return self.send()

    def send(self) -> RestpiteResponse:
        with RespiteClient(**self._client_dict()) as client:
            return client.request(self.method, self.url)

    def _client_dict(self) -> Dict[Any, Any]:
        return {
            "headers": self.headers,
            "handlers": self.handlers,
            "timeout": self.timeout,
            "params": self.params,
            "verify": self.verify,
            "auth": self.auth,
            "use_async": self.use_async,
            "http2": self.http2,
        }


http_get = partial(RestpiteRequest, method=GET)
http_post = partial(RestpiteRequest, method=POST)
http_put = partial(RestpiteRequest, method=PUT)
http_delete = partial(RestpiteRequest, method=DELETE)
http_patch = partial(RestpiteRequest, method=PATCH)
