from __future__ import annotations

import logging
from typing import Dict
from typing import List
from typing import Optional

from requests import Session

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

    :param headers: A dictionary of headers to include in all session requests.
    :param listeners: Optional implementations of the `AbstractHttpListener` interface
    :param connection_timeout: How long we will wait for your client to establish a remote connection, defaults to 31.00
    :param read_timeout: How long we will wait for the server to send a response, defaults to 31.00
    :param query_strings: A mapping of strings to indicate query string parameters, appended to all request urls
    """

    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        listeners: Optional[List[builtin_listeners.AbstractHttpListener]] = None,
        connection_timeout: float = 31.00,
        read_timeout: float = 31.00,
        query_strings: Optional[Dict[str, str]] = None,
    ) -> None:
        self.headers = headers
        self.listeners = [] if listeners is None else listeners.copy()
        self.listeners.insert(0, builtin_listeners.LoggingListener())
        self.connection_timeout = connection_timeout
        self.read_timeout = read_timeout
        self.query_strings = query_strings
        self.session = Session()
