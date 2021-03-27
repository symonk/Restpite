from __future__ import annotations

import logging
import pathlib
import typing

import requests

from restpite.__version__ import __version__
from restpite.http import interfaces
from restpite.listeners import builtin_listeners

log = logging.getLogger(__name__)


class RestpiteSession:
    """
    The bread and butter of restpite.  Used for persisting session data across multiple
    HTTP requests.  In it's simplest form even simple requests create a single-use
    session under the hood.

    Inline with the TCP packet retransmission window, restpite defaults both timeouts to slightly over
    a multiple of 3 for both connection and read timeouts respectively.

    Restpite Session uses a `requests.Session` under the hood for now.

    :param additional_headers: A dictionary of headers to include in all session requests.  These are applied
    on top of the requests default headers  which are:

        `User-Agent` = `restpite-{respite-version}`
        `Accept-Encoding` = `gzip, deflate`
        `Accept` = `*/*` (anything)
        `Connection` = `Keep-Alive`


    :param listeners: Optional implementations of the `AbstractHttpListener` interface
    :param connection_timeout: How long we will wait for your client to establish a remote connection, defaults to 31.00
    :param read_timeout: How long we will wait for the server to send a response, defaults to 31.00
    :param query_strings: A mapping of strings to indicate query string parameters, appended to all request urls
    :param defer_response_body: Defer the downloading response bodies until response.content is accessed.  Care is
    advised here as sessions will not be re-allocated back to the pool until the response body has been downloaded.
    :param ssl_verification: Verify SSL certificates, raises a SSLError otherwise, defaults to True.  Supports
    passing a file path to either a CA_BUNDLE or directory with a certificates of trusted CAs as well as boolean.
    As per requests standard, directories of certificates here must of been parsed with the `c_rehash` utility
    supplied by OpenSSL.
    :param maximum_redirects_limit: integer of how many redirects requests permits before raising a
    `TooManyRedirects` exception.
    :param transport_adapters: List of additional transport adapters to mount on the HTTP session.  By default
    session ships with a simple `requests.adapter.HTTPAdapter` listening for all traffic on both http
    and https respectively.
    :param user_agent: The User Agent string added to subsequent request headers, if omitted restpite will
    replace the user-agent header with its own using `restpite-{restpite-version}`.
    """

    def __init__(
        self,
        additional_headers: typing.Optional[typing.Dict[str, str]] = None,
        listeners: typing.Optional[
            typing.List[builtin_listeners.AbstractHttpListener]
        ] = None,
        connection_timeout: float = 31.00,
        read_timeout: float = 31.00,
        query_strings: typing.Optional[typing.Dict[str, str]] = None,
        defer_response_body: bool = False,
        ssl_verification: typing.Optional[typing.Union[bool, pathlib.Path, str]] = True,
        maximum_redirects_limit: int = 30,
        transport_adapters: typing.Optional[typing.List[interfaces.Mountable]] = None,
        user_agent: typing.Optional[str] = None,
    ) -> None:
        self.headers = additional_headers
        self.listeners = [] if listeners is None else listeners.copy()
        self.listeners.insert(0, builtin_listeners.LoggingListener())
        self.connection_timeout = connection_timeout
        self.read_timeout = read_timeout
        self.query_strings = query_strings
        self.defer_response_body = defer_response_body
        self.ssl_verification = ssl_verification
        self.maximum_redirects_limit = maximum_redirects_limit
        self.transport_adapters = transport_adapters or []
        self.user_agent = user_agent or f"restpite={__version__}"
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
        session.headers.update(self.headers)  # type: ignore [arg-type]
        # TODO: Finish session creation! (Fix header merging too, its broken)
        return session
