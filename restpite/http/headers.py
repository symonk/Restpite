import abc
import typing


class IHeader(abc.ABC):
    def __init__(self, headers: typing.MutableMapping[str, typing.Any]) -> None:
        self.headers = headers

    @abc.abstractmethod
    def resolve_headers(self, default_headers: typing.MutableMapping[str, typing.Any]):
        ...


class MergeHeaders(IHeader):
    """
    Implementation of headers to merge user provided headers along with the
    requests default headers.
    """

    def __init__(self, headers: typing.MutableMapping[str, typing.Any]) -> None:
        super().__init__(headers)

    def resolve_headers(self, default_headers: typing.MutableMapping[str, typing.Any]):
        default_headers.update(self.headers)
        return default_headers


class OnlyHeaders(IHeader):
    """
    Implementation of headers to wipe the request default headers and use
    only the user provided headers, useful for testing edge cases where
    having requests insert headers implicitly on the users behalf.
    """

    def __init__(self, headers: typing.MutableMapping[str, typing.Any]) -> None:
        super().__init__(headers)

    def resolve_headers(self, default_headers: typing.MutableMapping[str, typing.Any]):
        return self.headers
