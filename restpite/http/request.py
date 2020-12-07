from __future__ import annotations

from typing import Mapping
from typing import Optional
from urllib.parse import urlencode

from restpite import RestpiteConfig


class Request:
    def __init__(
        self, url: str, method: str = "get", config: Optional[RestpiteConfig] = None
    ) -> None:
        self.url = url
        self.qs_params: Optional[Mapping[str, str]] = None
        self.headers: Optional[Mapping[str, str]] = None
        self.method = method.lower()
        self.request = None
        self.config = config
        self._raise_on_failure = False
        self.retries = 0

    def _build_url(self, qs_params: Mapping[str, str]) -> str:
        """
        Encode query string params dictionary and append it to the URL.
        :param qs_params: Dictionary of k:v pairs to url encode and append to the url.
        :returns: Resolved url including query string params.
        """
        return self.url if not qs_params else f"{self.url}?{urlencode(qs_params)}"

    def raise_on_failure(self) -> Request:
        self._raise_on_failure = True
        return self

    def retry(self, times: int = 0) -> Request:
        self.retries = times
        return self

    def with_query_params(self, qs_params: Mapping[str, str]) -> Request:
        """
        Append query string params to the When request object.
        Resolve the url correctly given the data provided for the query string.
        :param qs_params: Dictionary of k:v pairs to url encode and append to the url.
        :returns: The (self) when request object for fluency.
        """
        self.qs_params = qs_params
        self.url = self._build_url(qs_params)
        return self

    def with_headers(self, headers: Mapping[str, str]) -> Request:
        """
        Append the given headers dictionary into the request headers.
        :param headers: Key:Value map object of headers.
        :returns: The (self) when request object for fluency.
        """
        self.headers = headers
        return self

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

    def send(self) -> Response:
        # Fire the request, grab the response!
        # Build a Response/Then instance
        ...


class Response:
    def __init__(self) -> None:
        self.status_code = 200
