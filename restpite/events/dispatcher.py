import contextlib
from typing import List

from .event_protocols import NotifyProtocol


class EventDispatcher:
    def __init__(self) -> None:
        self.handlers: List[NotifyProtocol] = []

    def subscribe(self, handler: NotifyProtocol) -> None:
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unsubscribe(self, handler: NotifyProtocol) -> None:
        with contextlib.suppress(ValueError):
            self.handlers.remove(handler)

    def dispatch(self, method: str, *args, **kwargs) -> None:
        for handler in reversed(self.handlers):
            func = getattr(handler, method, None)
            if func is not None:
                func(*args, **kwargs)
