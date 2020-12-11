from __future__ import annotations

from typing import Any
from typing import Callable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Type
from urllib.parse import urlencode

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from restpite import RestpiteConfig


class RestpiteSession:
    def __init__(
        self, retry: Optional[Tuple[int, float, List[int], Type[BaseException]]] = None
    ):
        self._session: Session = Session()
        if retry:
            total, backoff, statuses, exc = retry
            retries = Retry(
                total=total, backoff_factor=backoff, status_forcelist=statuses
            )
            self._session.mount("http://", HTTPAdapter(max_retries=retries))
            self._session.mount("https://", HTTPAdapter(max_retries=retries))

    def get(self, url, **kwargs):
        self._session.get(url, **kwargs)

    def __enter__(self) -> RestpiteSession:
        return self

    def __exit__(self, *args) -> None:
        self._session.close()


class Request:
    def __init__(
        self,
        url: str,
        query_params: Optional[Mapping[str, str]] = None,
        config: Optional[RestpiteConfig] = None,
        raise_on_failure: bool = False,
        retryable: Optional[Tuple[int, Type[BaseException]]] = None,
        headers: Optional[Mapping[str, str]] = None,
        hooks: Optional[List[Callable[[Any], Any]]] = None,
        connect_timeout: float = 10,
        read_timeout: float = 10,
    ) -> None:
        self.url: str = self.url if not query_params else self._build_url(
            url, query_params
        )
        self.config = config
        self.raise_on_failure = raise_on_failure
        self.retryable = retryable
        self.headers = headers
        self.hooks = hooks
        self.timeout = (connect_timeout, read_timeout)

    @staticmethod
    def _build_url(url: str, qs_params: Mapping[str, str]) -> str:
        """
        Encode query string params dictionary and append it to the URL.
        :param qs_params: Dictionary of k:v pairs to url encode and append to the url.
        :returns: Resolved url including query string params.
        """
        return url if not qs_params else f"{url}?{urlencode(qs_params)}"

    def get(self) -> Response:
        """
        Configure the request method to HTTP GET
        """
        return self._dispatch("get")

    def options(self) -> Response:
        """
        Configure the request method to HTTP OPTIONS
        """
        return self._dispatch("options")

    def head(self) -> Response:
        """
        Configure the request method to HTTP HEAD
        """
        return self._dispatch("head")

    def post(self) -> Response:
        """
        Configure the request method to HTTP POST
        """
        return self._dispatch("post")

    def put(self) -> Response:
        """
        Configure the request method to HTTP PUT
        """
        return self._dispatch("put")

    def patch(self) -> Response:
        """
        Configure the request method to HTTP PATCH
        """
        return self._dispatch("patch")

    def delete(self) -> Response:
        """
        Configure the request method to HTTP DELETE
        """
        return self._dispatch("delete")

    @staticmethod
    def _dispatch(method: str = "get") -> Response:
        return Response()


class Response:
    def __init__(self) -> None:
        self.status_code = 200
