from typing import Protocol

from restpite import RestpiteResponse


class NotifyProtocol(Protocol):
    """
    Custom protocol for inspecting Restpite request and responses (and others) at runtime in order
    to drop in and control or manipulate the data.
    """

    def before_sending_request(self) -> None:
        ...

    def after_receiving_response(self, response: RestpiteResponse) -> None:
        ...

    def on_exception(self, exc: BaseException) -> None:
        ...
