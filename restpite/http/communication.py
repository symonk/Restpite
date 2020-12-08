from __future__ import annotations

from typing import Any
from typing import Callable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Type
from urllib.parse import urlencode

from restpite import RestpiteConfig


class Session:
    ...


class Request:
    def __init__(
        self,
        url: str,
        query_params: Optional[Mapping[str, str]] = None,
        method: str = "get",
        config: Optional[RestpiteConfig] = None,
        raise_on_failure: bool = False,
        retryable: Optional[Tuple[int, Type[BaseException]]] = None,
        headers: Optional[Mapping[str, str]] = None,
        hooks: Optional[List[Callable[[Any], Any]]] = None,
    ) -> None:
        self.url: str = self.url if not query_params else self._build_url(
            url, query_params
        )
        self.method = method
        self.config = config
        self.raise_on_failure = raise_on_failure
        self.retryable = retryable
        self.headers = headers
        self.hooks = hooks

    @staticmethod
    def _build_url(url: str, qs_params: Mapping[str, str]) -> str:
        """
        Encode query string params dictionary and append it to the URL.
        :param qs_params: Dictionary of k:v pairs to url encode and append to the url.
        :returns: Resolved url including query string params.
        """
        return url if not qs_params else f"{url}?{urlencode(qs_params)}"

    def get(self) -> Request:
        """
        Configure the request method to HTTP GET
        """
        self.method = "get"
        return self

    def options(self) -> Request:
        """
        Configure the request method to HTTP OPTIONS
        """
        self.method = "options"
        return self

    def head(self) -> Request:
        """
        Configure the request method to HTTP HEAD
        """
        self.method = "head"
        return self

    def post(self) -> Request:
        """
        Configure the request method to HTTP POST
        """
        self.method = "post"
        return self

    def put(self) -> Request:
        """
        Configure the request method to HTTP PUT
        """
        self.method = "put"
        return self

    def patch(self) -> Request:
        """
        Configure the request method to HTTP PATCH
        """
        self.method = "patch"
        return self

    def delete(self) -> Request:
        """
        Configure the request method to HTTP DELETE
        """
        self.method = "delete"
        return self

    def fire(self) -> Response:
        # Fire the request, grab the response!
        # Build a Response/Then instance
        return Response()


class Response:
    def __init__(self) -> None:
        self.status_code = 200
