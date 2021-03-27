from typing import Protocol


class RestpiteListener(Protocol):
    """
    Custom Protocol for creating user defined listeners.  Listeners can be passed into a
    `Restpite.Session` and are executed in LIFO order at runtime.
    """

    def before_sending_request(self) -> None:
        ...

    def after_receiving_response(self) -> None:
        ...

    def on_exception(self, exc: BaseException) -> None:
        ...
