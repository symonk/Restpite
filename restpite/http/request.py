from __future__ import annotations

from typing import Mapping
from typing import Optional
from urllib.parse import urlencode

from requests import Response

from restpite import RestpiteConfig


class When:
    def __init__(
        self, url: str, method: str = "get", config: Optional[RestpiteConfig] = None
    ) -> None:
        self.url = url
        self.qs_params: Optional[Mapping[str, str]] = None
        self.headers: Optional[Mapping[str, str]] = None
        self.method = method.lower()
        self.request = None
        self.config = config

    def _build_url(self, qs_params: Mapping[str, str]) -> str:
        """
        Encode query string params dictionary and append it to the URL.
        :param qs_params: Dictionary of k:v pairs to url encode and append to the url.
        :returns: Resolved url including query string params.
        """
        return self.url if not qs_params else f"{self.url}?{urlencode(qs_params)}"

    def with_query_params(self, qs_params: Mapping[str, str]) -> When:
        """
        Append query string params to the When request object.
        Resolve the url correctly given the data provided for the query string.
        :param qs_params: Dictionary of k:v pairs to url encode and append to the url.
        :returns: The (self) when request object for fluency.
        """
        self.qs_params = qs_params
        self.url = self._build_url(qs_params)
        return self

    def with_headers(self, headers: Mapping[str, str]) -> When:
        """
        Append the given headers dictionary into the request headers.
        :param headers: Key:Value map object of headers.
        :returns: The (self) when request object for fluency.
        """
        self.headers = headers
        return self

    def get(self) -> When:
        """
        Configure the request method to HTTP GET
        """
        self.method = "get"
        return self

    def options(self) -> When:
        """
        Configure the request method to HTTP OPTIONS
        """
        self.method = "options"
        return self

    def head(self) -> When:
        """
        Configure the request method to HTTP HEAD
        """
        self.method = "head"
        return self

    def post(self) -> When:
        """
        Configure the request method to HTTP POST
        """
        self.method = "post"
        return self

    def put(self) -> When:
        """
        Configure the request method to HTTP PUT
        """
        self.method = "put"
        return self

    def patch(self) -> When:
        """
        Configure the request method to HTTP PATCH
        """
        self.method = "patch"
        return self

    def delete(self) -> When:
        """
        Configure the request method to HTTP DELETE
        """
        self.method = "delete"
        return self

    def then(self) -> Then:
        # Fire the request, grab the response!
        # Build a Response/Then instance
        ...


class Given:
    def __init__(self, raise_when_unsuccessful: bool = False, retry: int = 0) -> None:
        # configurations happen here
        self.raise_when_unsuccessful = raise_when_unsuccessful
        self._retry = retry

    def when(self, *args, **kwargs) -> When:
        return When(*args, **kwargs)

    def retry(self, times: int = 0) -> Given:
        self._retry = times
        return self


class Then:
    def __init__(self, response: Response) -> None:
        self.response = response


given = Given
