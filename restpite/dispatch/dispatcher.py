import contextlib
from typing import List

from restpite.protocols.restpite_protocols import Notifyable


class HandlerDispatcher:
    def __init__(self) -> None:
        self.handlers: List[Notifyable] = []

    def subscribe(self, handler: Notifyable) -> None:
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler: Notifyable) -> None:
        with contextlib.suppress(ValueError):
            self.handlers.remove(handler)

    def dispatch(self, method: str, *args, **kwargs) -> None:
        for handler in reversed(self.handlers):
            func = getattr(handler, method, None)
            if func is not None:
                func(*args, **kwargs)
