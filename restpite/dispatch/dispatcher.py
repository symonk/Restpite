import collections
import contextlib
from typing import Any
from typing import Deque

from restpite.protocols.restpite_protocols import Notifyable


class HandlerDispatcher:
    def __init__(self) -> None:
        self.handlers: Deque[Notifyable] = collections.deque()

    def subscribe(self, handler: Notifyable) -> None:
        """
        Register a new handler that implements the Notifyable protocol
        :param handler: Notifyable instance to append to callbacks.
        """
        if not isinstance(handler, Notifyable):
            # TODO: Is this pythonic? Since it is called much later down stream I think a check here is appropriate.
            raise TypeError(
                f"Type of handle was: {type(handler)}, it should be: {type(Notifyable)}"
            )
        if handler not in self.handlers:
            self.handlers.appendleft(handler)

    def unsubscribe(self, handler: Notifyable) -> None:
        """
        Attempt to remove a callback from the list of stored callbacks.
        ValueErrors are suppressed and None is returned if the handler was not previously registered.
        :param handler: Notifyable instance to remove
        """
        with contextlib.suppress(ValueError):
            self.handlers.remove(handler)

    def reset(self) -> None:
        """
        Delete all the current handlers (if any exist)
        """
        self.handlers.clear()

    def dispatch(self, method: str, *args: Any, **kwargs: Any) -> None:
        """
        Dispatches function calls to all handlers.  By default these handlers are executed in
        LIFO order.  `RestpiteSession` objects dispatch to their registered handlers here,
        invoking the well defined methods of the Notifyable Protocol.
        """
        for handler in self.handlers:
            func = getattr(handler, method, None)
            if func is not None:
                # TODO: Does this need guarded? should we let python raise the TypeError (None is not callable?)
                func(*args, **kwargs)
