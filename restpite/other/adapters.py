import abc
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Union

from requests.adapters import HTTPAdapter
from requests.status_codes import _codes as status_codes  # type: ignore
from urllib3 import Retry


class Mountable(abc.ABC):
    def __init__(self, prefix: str, adapter=None):
        self.prefix = prefix
        self.adapter = adapter

    def __iter__(self):
        return iter((self.prefix, self.adapter))


class RetryAdapter(Mountable):
    def __init__(
        self,
        prefix,
        max_attempts: int = 5,
        connect: Optional[int] = None,
        read: Optional[int] = None,
        redirect: Optional[int] = None,
        status: Optional[int] = None,
        other: Optional[int] = None,
        allowed_methods: Iterable[str] = Retry.DEFAULT_ALLOWED_METHODS,
        until_status_in: Optional[Union[int, Iterable[int]]] = None,
        backoff_factor: Optional[float] = 1,
        raise_on_redirect: bool = True,
        raise_on_status: bool = True,
        history: Optional[Tuple[str]] = None,
        respect_retry_after_header: bool = False,
        remove_headers_on_redirect: bool = False,
    ):
        super().__init__(prefix)
        allowed = (
            [until_status_in]
            if not isinstance(until_status_in, Iterable)
            else until_status_in
        )
        status_forcelist = [x for x in status_codes if x not in allowed]
        self.retry = Retry(
            max_attempts,
            connect,
            read,
            redirect,
            status,
            other,
            allowed_methods,
            status_forcelist,
            backoff_factor,
            raise_on_redirect,
            raise_on_status,
            history,
            respect_retry_after_header,
        )
        self.adapter = HTTPAdapter(max_retries=self.retry)
