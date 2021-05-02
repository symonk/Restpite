from typing import Protocol
from typing import runtime_checkable

from httpx import Request

from restpite.http.response import RestpiteResponse


@runtime_checkable
class Notifyable(Protocol):
    """
    Custom protocol for inspecting Restpite request and responses (and others) at runtime in order
    to drop in and control or manipulate the data.
    """

    def before_sending_request(
        self,
        request: Request,
        method,
        url,
        content,
        data,
        files,
        json,
        params,
        headers,
        cookies,
    ) -> None:
        ...

    def after_receiving_response(self, response: RestpiteResponse) -> None:
        ...

    def on_exception(self, exc: BaseException) -> None:
        ...
