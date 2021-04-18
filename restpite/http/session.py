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

from restpite import Notifyable
from restpite import RestpiteResponse
from restpite import __version__
from restpite.dispatch.dispatcher import HandlerDispatcher
from restpite.http.http_types import HTTP_AUTH_ALIAS
from restpite.http.http_types import HTTP_CONTENT_ALIAS
from restpite.http.http_types import HTTP_COOKIES_ALIAS
from restpite.http.http_types import HTTP_DATA_ALIAS
from restpite.http.http_types import HTTP_FILES_ALIAS
from restpite.http.http_types import HTTP_HEADERS_ALIAS
from restpite.http.http_types import HTTP_JSON_ALIAS
from restpite.http.http_types import HTTP_QUERY_STRING_ALIAS
from restpite.http.http_types import HTTP_TIMEOUT_ALIAS
from restpite.http.http_types import HTTP_URLTYPES_ALIAS

log = logging.getLogger(__name__)


class RespiteClient:
    """

    # TODO: How can we dispatch both listener calls and events to user defined 'observers'?
    # TODO: This would be pretty powerful and allow clients to register their own observers to
    # TODO: The session, which would be notified on particular actions (listening, hooks, events etc).

    The bread and butter of restpite.  Used for persisting session data across multiple
    HTTP requests.  In it's simplest form even simple requests create a single-use
    session under the hood.

    Inline with the TCP packet retransmission window, restpite defaults both timeouts to slightly over
    a multiple of 3 for both connection and read timeouts respectively.

    Restpite Session uses a `requests.Session` under the hood for now.

    :param headers: A dictionary of headers to include in all session requests.  These are applied
    on top of the requests default headers  which are:

        `User-Agent` = `restpite-{respite-version}`
        `Accept-Encoding` = `gzip, deflate`
        `Accept` = `*/*` (anything)
        `Connection` = `Keep-Alive`


    :param connection_timeout: How long we will wait for your client to establish a remote connection, defaults to 31.00
    :param read_timeout: How long we will wait for the server to send a response, defaults to 31.00
    :param params: A mapping of strings to indicate query string parameters, appended to all request urls
    :param stream: Defer the downloading response bodies until response.content is accessed.  Care is
    advised here as sessions will not be re-allocated back to the pool until the response body has been downloaded.
    :param verify: Verify SSL certificates, raises a SSLError otherwise, defaults to True.  Supports
    passing a file path to either a CA_BUNDLE or directory with a certificates of trusted CAs as well as boolean.
    As per requests standard, directories of certificates here must of been parsed with the `c_rehash` utility
    supplied by OpenSSL.
    :param max_redirects: integer of how many redirects requests permits before raising a
    `TooManyRedirects` exception.
    :param adapters: List of additional transport adapters to mount on the HTTP session.  By default
    session ships with a simple `requests.adapter.HTTPAdapter` listening for all traffic on both http
    and https respectively.
    :param user_agent: The User Agent string added to subsequent request headers, if omitted restpite will
    replace the user-agent header with its own using `restpite-{restpite-version}`.
    :param auth: Callable for a custom authentication to pass to requests.  Subclassing
    `requests.auth.Authbase` is advisable here.  Restpite also provides some implementations out of the box.
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
    ) -> None:
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
        self.client = self._prepare_client()

    def __getattr__(self, item: str) -> Any:
        """
        Proxy unknown attribute lookups onto the underlying `requests.Session` instance.
        Eventually a full API will be exposed by restpite to make this redundant but this
        will suffice for while, the plan is to expose a fully typed equivalent.  This is
        not a full `Proxy` but a mere 'do for now' while in the alpha stages, more to be
        investigated on this later.
        """
        return getattr(self.client, item)

    def _prepare_client(self) -> httpx.Client:
        """
        Requests Session objects cannot be instantiated using some of the supported arguments of
        restpite, restpite makes this a little easier for users who want to set some 'global' values
        when instantiating a `RestpiteSession` where the delegating is handled here.
        """
        session = httpx.Client()
        session.verify = self.verify
        session.params = self.params
        session.headers.update(self.headers)
        session.auth = self.auth
        # TODO: Finish session delegation
        # TODO: Missing (proxies, hooks, cert, trust_env, cookies, adapters)
        return session

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
        # TODO: Implement the full flow on HTTP GETs here, then we can build on it. but it should account
        # TODO: For both listener and event/hook dispatching
        """
        Issue a HTTP GET request
        """
        return self.request("GET", url, *args, **kwargs)
