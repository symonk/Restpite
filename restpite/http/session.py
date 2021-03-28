from __future__ import annotations

import logging
import types
import typing

import requests
from requests.auth import AuthBase

from restpite.__version__ import __version__
from restpite.http import http_protocols
from restpite.listeners import listener_protocols
from restpite.listeners import listeners as builtin_listeners

log = logging.getLogger(__name__)


class RestpiteSession:
    """
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


    :param listeners: Optional implementations of the `RestpiteListener` Protocol
    :param connection_timeout: How long we will wait for your client to establish a remote connection, defaults to 31.00
    :param read_timeout: How long we will wait for the server to send a response, defaults to 31.00
    :param params: A mapping of strings to indicate query string parameters, appended to all request urls
    :param stream: Defer the downloading response bodies until response.content is accessed.  Care is
    advised here as sessions will not be re-allocated back to the pool until the response body has been downloaded.
    :param verify: Verify SSL certificates, raises a SSLError otherwise, defaults to True.  Supports
    passing a file path to either a CA_BUNDLE or directory with a certificates of trusted CAs as well as boolean.
    As per requests standard, directories of certificates here must of been parsed with the `c_rehash` utility
    supplied by OpenSSL.
    :param maximum_redirects_limit: integer of how many redirects requests permits before raising a
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
        headers: typing.Optional[typing.Dict[str, str]] = None,
        listeners: typing.Optional[
            typing.List[listener_protocols.RestpiteListener]
        ] = None,
        connection_timeout: float = 31.00,
        read_timeout: float = 31.00,
        params: typing.Optional[
            typing.Union[bytes, typing.MutableMapping[str, str]]
        ] = None,
        stream: bool = False,
        verify: typing.Union[bool, str] = True,
        maximum_redirects_limit: int = 30,
        adapters: typing.Optional[typing.List[http_protocols.Mountable]] = None,
        user_agent: typing.Optional[str] = None,
        auth: typing.Optional[
            typing.Union[
                typing.Tuple[str, str],
                AuthBase,
                typing.Callable[[requests.Request], requests.Request],
            ]
        ] = None,
    ) -> None:
        self.headers = headers or {}
        if user_agent:
            self.headers["User-Agent"] = user_agent or f"restpite-{__version__}"
        self.listeners = [] if listeners is None else listeners.copy()
        self.listeners.insert(0, builtin_listeners.LoggingListener())
        self.connection_timeout = connection_timeout
        self.read_timeout = read_timeout
        self.query_strings = params or {}
        self.defer_response_body = stream
        self.verify = verify
        self.max_redirects = maximum_redirects_limit
        self.adapters = adapters or []
        self.auth = auth
        self.session = self._prepare_session()

    def __getattr__(self, item: str) -> typing.Any:
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
        session.params = self.query_strings
        session.headers.update(self.headers)
        session.auth = self.auth
        # TODO: Finish session delegation
        # TODO: Missing (proxies, hooks, cert, trust_env, cookies, adapters)
        return session

    def __enter__(self) -> RestpiteSession:
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_value: typing.Optional[BaseException] = None,
        traceback: typing.Optional[types.TracebackType] = None,
    ) -> None:
        self.session.close()
