from __future__ import annotations

import logging
from types import TracebackType
from typing import Any
from typing import AnyStr
from typing import Callable
from typing import Iterable
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Type

from requests import RequestException
from requests import Response
from requests import Session

from restpite.http.adapters import Mountable
from restpite.http.listeners import AbstractHttpListener
from restpite.http.response import HttpResponse

log = logging.getLogger(__name__)


class HttpSession:
    """
    The core HttpSession object of Restpite.  HttpSession is a subclass of `requests.Session`
    but exposes some user-friendly and test-friendly pieces of functionality to the user
    automatically.

    :param headers (MutableMapping): Mapping of additional headers to be sent with every subsequent request
    of the given session.
    """

    def __init__(
        self,
        headers: Optional[MutableMapping[str, str]] = None,
        connection_timeout: float = 30.00,
        read_timeout: float = 15.00,
        listeners: Optional[Sequence[AbstractHttpListener]] = None,
        adapters: Optional[Iterable[Mountable]] = None,
        hooks: Optional[Iterable[Callable[[Any], Any]]] = None,
        verify: bool = True,
        stream: bool = False,
    ):
        self.session = Session()
        self.connection_timeout = connection_timeout
        self.read_timeout = read_timeout
        self.listeners = listeners or []
        self.hooks = hooks
        self.verify = verify
        self.stream = stream
        if headers:
            self.headers.update(**headers)
        self._register_adapters(adapters)

    @property
    def headers(self):
        return self.session.headers

    def _dispatch(self, method: str, *args, **kwargs) -> Response:
        """
        Routes the HTTPSessions calls through requests directory, permitting the
        invocation of user defined listeners before and after requesting.  Listener
        calls are executed in FIFO order
        """
        self._execute_listeners_command("before_send_request", *args, **kwargs)
        try:
            response = getattr(self.session, method)(*args, **kwargs)
            assert isinstance(response, Response)
            self._execute_listeners_command("after_retrieve_response", response)
            return response
        except RequestException:
            self._execute_listeners_command("on_request_exception")
            raise

    def _execute_listeners_command(self, func_name: str, *args, **kwargs) -> None:
        for listener in self.listeners:
            getattr(listener, func_name)(*args, **kwargs)

    def _register_adapters(
        self, adapters: Optional[Iterable[Mountable]]
    ) -> HttpSession:
        for adapter in adapters or []:
            self.session.mount(*adapter)
        return self

    def http_get(self, url: AnyStr, **kwargs) -> HttpResponse:
        return HttpResponse(self._dispatch("get", url, **kwargs))

    def __enter__(self) -> HttpSession:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        self.session.close()
