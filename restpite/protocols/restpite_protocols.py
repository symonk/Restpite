from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable


@runtime_checkable
class Curlable(Protocol):
    def curlify(self) -> str:
        """
        Converts the object into a curl string, used for recreating the request
        """
        ...


class Assertable(Protocol):
    def raise_assertion_failure(self, message: str) -> None:
        ...
