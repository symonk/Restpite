from __future__ import annotations

import logging
import types
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import MutableMapping
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

import requests
from requests.auth import AuthBase

from restpite import Notifyable
from restpite import RestpiteResponse
from restpite import __version__
from restpite.dispatch.dispatcher import HandlerDispatcher

log = logging.getLogger(__name__)


class RestpiteSession:
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
        headers: Optional[Dict[str, str]] = None,
        handlers: Optional[List[Notifyable]] = None,
        connection_timeout: float = 31.00,
        read_timeout: float = 31.00,
        params: Optional[Union[bytes, MutableMapping[str, str]]] = None,
        stream: bool = False,
        verify: Union[bool, str] = True,
        max_redirects: int = 30,
        adapters: Optional[List[Notifyable]] = None,
        user_agent: Optional[str] = None,
        auth: Optional[
            Union[
                Tuple[str, str],
                AuthBase,
                Callable[[requests.Request], requests.Request],
            ]
        ] = None,
    ) -> None:
        self.headers = headers or {}
        self.headers["User-Agent"] = (
            f"restpite-{__version__}" if not user_agent else user_agent
        )
        self.connection_timeout = connection_timeout
        self.read_timeout = read_timeout
        self.params = params or {}
        self.defer_response_body = stream
        self.verify = verify
        self.max_redirects = max_redirects
        self.adapters = adapters or []
        self.auth = auth
        self.handler_dispatcher = HandlerDispatcher()
        handlers = handlers.copy() if handlers is not None else []
        for handler in handlers:
            self.handler_dispatcher.subscribe(handler)
        self.session = self._prepare_session()

    def __getattr__(self, item: str) -> Any:
        """
        Proxy unknown attribute lookups onto the underlying `requests.Session` instance.
        Eventually a full API will be exposed by restpite to make this redundant but this
        will suffice for while, the plan is to expose a fully typed equivalent.  This is
        not a full `Proxy` but a mere 'do for now' while in the alpha stages, more to be
        investigated on this later.
        """
        return getattr(self.session, item)

    def _prepare_session(self) -> requests.Session:
        """
        Requests Session objects cannot be instantiated using some of the supported arguments of
        restpite, restpite makes this a little easier for users who want to set some 'global' values
        when instantiating a `RestpiteSession` where the delegating is handled here.
        """
        session = requests.Session()
        session.stream = self.defer_response_body
        session.verify = self.verify
        session.max_redirects = self.max_redirects
        session.params = self.params
        session.headers.update(self.headers)
        session.auth = self.auth
        # TODO: Finish session delegation
        # TODO: Missing (proxies, hooks, cert, trust_env, cookies, adapters)
        return session

    def __enter__(self) -> RestpiteSession:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[types.TracebackType] = None,
    ) -> None:
        self.session.close()

    def request(
        self,
        method: str,
        url: str,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=None,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
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
                self.session.request(
                    method,
                    url,
                    params,
                    data,
                    headers,
                    cookies,
                    files,
                    auth,
                    timeout,
                    allow_redirects,
                    proxies,
                    hooks,
                    stream,
                    verify,
                    cert,
                    json,
                )
            )
            self.handler_dispatcher.dispatch("after_receiving_response", response)
            return response
        except Exception as exc:
            # TODO: Too broad!
            self.handler_dispatcher.dispatch("on_exception", exc)
            raise exc from None

    def get(
        self,
        url: str,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=None,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> RestpiteResponse:
        # TODO: Implement the full flow on HTTP GETs here, then we can build on it. but it should account
        # TODO: For both listener and event/hook dispatching
        """
        Issue a HTTP GET request
        """
        return self.request(
            "get",
            url,
            params,
            data,
            headers,
            cookies,
            files,
            auth,
            timeout,
            allow_redirects,
            proxies,
            hooks,
            stream,
            verify,
            cert,
            json,
        )
