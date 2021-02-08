from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional

from requests import Session

from restpite.http.adapters import Mountable
from restpite.http.headers import IHeader
from restpite.http.listeners import AbstractHttpListener


class HttpSession(Session):
    def __init__(
        self,
        headers: Optional[IHeader] = None,
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
        self._register_adapters(adapters)
        self._resolve_headers(headers)

    def _dispatch(self) -> None:
        ...

    def _register_adapters(
        self, adapters: Optional[Iterable[Mountable]]
    ) -> HttpSession:
        for adapter in adapters or []:
            self.mount(*adapter)
        return self

    def _resolve_headers(self, headers: Optional[IHeader]) -> HttpSession:
        self.headers = (
            headers.resolve_headers(self.headers) if headers else self.headers
        )
        return self

    def get(self, *args, **kwargs):
        kwargs["headers"] = self.headers
        return super().get(*args, **kwargs)
