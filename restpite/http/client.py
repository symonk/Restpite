from __future__ import annotations

import logging
import types
from typing import Any
from typing import List
from typing import Optional
from typing import Type
from typing import Union

import httpx
from httpx import Headers
from httpx._client import BaseClient

from restpite import Notifyable
from restpite import RestpiteResponse
from restpite import __version__
from restpite.dispatch.dispatcher import HandlerDispatcher
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

log = logging.getLogger(__name__)


class RespiteClient:
    """

    The bread and butter to restpite.  By default restpite operates on a synchronous nature, this is
    overridable by specifying `use_async` to `True` when instantiating a client instance.  It is possible to implement
    your own adapter instances and have restpite call them at runtime at various stages of the work flow.

    :param headers: A Mapping of header key:value pairs to be sent with every request for the life time of the
    client instance.
    :param handlers: A sequence of objects implementing the `Notifable` protocol.  Client will dispatch out to
    these instances are various times through the HTTP work flow, namely before request, after response and on exc.
    :param timeout: A tuple of up to four floats
        - the connection timeout
        - the read timeout
        - the write timeout
        - the connection pool timeout
    :param params: A Mapping of query string parameters, restpite will auto append ?a=1&b=2 etc
    :params verify: CA bundle required to verify the identity of the requested hosts, by default this is
    the default CA, however a path can be provided to a SSL certificate file also, or the verification can
    be disabled by passing False explicitly
    :params adapter: ...
    :params user_agent: A string to specify as the user agent for all outward requests, by default the user
    agent is set like so: `respite-{respite_version}`, setting this explicitly to False will remove the
    respite inbuilt user agent
    :params auth: ...
    :params use_async: Respite will provide an Asynchronous client, rather than a synchronous one
    :params http2: Restpite will attempt to communicate over the HTTP/2 protocol, however should the server
    not support HTTP/2, default HTTP/1 will be used, to see which version was used, inspecting the
    `Response.http_version` attr can be used.
    """

    def __init__(
        self,
        headers: HTTP_HEADERS_ALIAS = None,
        handlers: Optional[List[Notifyable]] = None,
        timeout: HTTP_TIMEOUT_ALIAS = None,
        params: HTTP_QUERY_STRING_ALIAS = None,
        verify: Union[bool, str] = True,
        adapters: Optional[List[Notifyable]] = None,
        user_agent: Optional[str] = None,
        auth: HTTP_AUTH_ALIAS = None,
        use_async: bool = False,
        http2: bool = False,
        base_url: HTTP_URLTYPES_ALIAS = None,
    ) -> None:
        self.use_async = use_async
        self.http2 = http2
        self.headers = headers or Headers()
        self.headers["User-Agent"] = (
            f"restpite-{__version__}" if not user_agent else user_agent
        )
        self.timeout = timeout
        self.params = params or {}
        self.verify = verify
        self.adapters = adapters or []
        self.auth = auth
        self.handler_dispatcher = HandlerDispatcher()
        handlers = handlers.copy() if handlers is not None else []
        for handler in handlers:
            self.handler_dispatcher.subscribe(handler)
        self.base_url = base_url
        self.client = self._prepare_client()

    def __getattr__(self, item: str) -> Any:
        """
        Proxy unknown attribute lookups onto the underlying `httpx.Client` instance.
        Eventually a full API will be exposed by restpite to make this redundant but this
        will suffice for while, the plan is to expose a fully typed equivalent.  This is
        not a full `Proxy` but a mere 'do for now' while in the alpha stages, more to be
        investigated on this later.
        """
        return getattr(self.client, item)

    def _prepare_client(self) -> BaseClient:
        """
        Based on various parameters of the RespiteClient instantiation, setup the low level
        client used for HTTP communication.  This is underpinned by httpx (no longer requests)
        and we can support both synchronous and asynchronous clients.
        """
        client = (
            httpx.Client(http2=self.http2)
            if not self.use_async
            else httpx.AsyncClient(http2=self.http2)
        )
        client.verify = self.verify
        client.params = self.params
        client.headers.update(self.headers)
        client.auth = self.auth
        # TODO: Finish client delegation
        # TODO: Missing (proxies, hooks, cert, trust_env, cookies, adapters)
        return client

    def __enter__(self) -> RespiteClient:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[types.TracebackType] = None,
    ) -> None:
        self.client.close()

    def request(
        self,
        method: str,
        url: HTTP_URLTYPES_ALIAS,
        *,
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
    ) -> RestpiteResponse:
        """
        Responsible for managing the actual HTTP Request from request -> Response
        # TODO: Understand these types (args)
        # TODO: Understand the proper flow of the traffic through the underlying requests library
        # TODO: Dispatching hooks mechanism around some of this
        # TODO: Hooks for raw request sending, raw response received, post RestpiteResponse, post RequestRequest
        # TODO: handlers = dispatching hook / calls to client code, adapter = transport adapters of requests
        # TODO: hooks need dispatched here multiple times, Hooks need invoked as well to permit control!
        # TODO: Built in capturing of all traffic, thinking simple `restpite.json` (configurable on|off) ?
        """
        try:
            self.handler_dispatcher.dispatch("before_sending_request")
            response = RestpiteResponse(
                self.client.request(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    allow_redirects=allow_redirects,
                    timeout=timeout,
                )
            )
            self.handler_dispatcher.dispatch("after_receiving_response", response)
            return response
        except Exception as exc:
            # TODO: Too broad!
            self.handler_dispatcher.dispatch("on_exception", exc)
            raise exc from None

    def get(self, url: HTTP_URLTYPES_ALIAS, *args, **kwargs) -> RestpiteResponse:
        """
        Issue a HTTP GET request
        """
        return self.request("GET", url, *args, **kwargs)
