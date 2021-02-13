from __future__ import annotations

import logging
from typing import Any
from typing import Callable
from typing import Iterable
from typing import MutableMapping
from typing import Optional

from requests import Session

from restpite.http.adapters import Mountable
from restpite.http.listeners import AbstractHttpListener

log = logging.getLogger(__name__)


class HttpSession(Session):
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
        listener: Optional[AbstractHttpListener] = None,
        adapters: Optional[Iterable[Mountable]] = None,
        hookz: Optional[Iterable[Callable[[Any], Any]]] = None,
        verify: bool = True,
        stream: bool = False,
    ):
        super().__init__()
        self.connection_timeout = connection_timeout
        self.read_timeout = read_timeout
        self.listener = listener
        self.hookz = hookz
        self.verify = verify
        self.stream = stream
        if headers:
            self.headers.update(**headers)
        self._register_adapters(adapters)

    def _dispatch(self) -> None:
        ...

    def _register_adapters(
        self, adapters: Optional[Iterable[Mountable]]
    ) -> HttpSession:
        for adapter in adapters or []:
            self.mount(*adapter)
        return self

    def get(self, *args, **kwargs):
        kwargs["headers"] = self.headers
        return super().get(*args, **kwargs)
