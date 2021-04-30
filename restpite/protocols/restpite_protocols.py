from typing import Protocol
from typing import runtime_checkable

from restpite import RestpiteResponse


@runtime_checkable
class Curlable(Protocol):
    def curlify(self) -> str:
        """
        Converts the object into a curl string, used for recreating the request
        """
        ...


@runtime_checkable
class Notifyable(Protocol):
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
