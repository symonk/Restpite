import collections
import contextlib
from typing import Any
from typing import Deque

from restpite.dispatch.dispatch_protocols import Notifyable


class HandlerDispatcher:
    def __init__(self) -> None:
        self._handlers: Deque[Notifyable] = collections.deque()

    def subscribe(self, handler: Notifyable) -> None:
        """
        Register a new handler that implements the Notifyable protocol
        :param handler: Notifyable instance to append to callbacks.
        """
        if handler not in self._handlers and isinstance(handler, Notifyable):
            self._handlers.appendleft(handler)

    def unsubscribe(self, handler: Notifyable) -> None:
        """
        Attempt to remove a callback from the list of stored callbacks.
        ValueErrors are suppressed and None is returned if the handler was not previously registered.
        :param handler: Notifyable instance to remove
        """
        with contextlib.suppress(ValueError):
            self._handlers.remove(handler)

    def reset(self) -> None:
        """
        Delete all the current handlers (if any exist)
        """
        self._handlers.clear()

    def dispatch(self, method_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Dispatches function calls to all handlers.  By default these handlers are executed in
        LIFO order.  `RestpiteSession` objects dispatch to their registered handlers here,
        invoking the well defined methods of the Notifyable Protocol.
        """
        for handler in self._handlers:
            attr = getattr(handler, method_name)
            attr(*args, **kwargs)
