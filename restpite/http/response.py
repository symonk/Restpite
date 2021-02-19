from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Type

from assertpy import assert_that
from requests import Response
from requests import codes as status_codes
from requests.utils import CaseInsensitiveDict


class HttpResponse:
    def __init__(self, wrapped_response: Response) -> None:
        self.wrapped_response = wrapped_response
        self.model: Optional[Any] = None

    @property
    def status_code(self) -> int:
        return self.wrapped_response.status_code

    @property
    def headers(self) -> CaseInsensitiveDict[Any]:
        return self.wrapped_response.headers

    def deserialize(self, model: Type[Any]) -> Any:
        return model(**self.wrapped_response.json())

    def assert_was_ok(self) -> HttpResponse:
        assert_that(self.status_code).is_equal_to(status_codes.ok)
        return self

    def assert_was_forbidden(self) -> HttpResponse:
        assert_that(self.status_code).is_equal_to(status_codes.forbidden)
        return self

    def had_status_code(self, expected_code: int) -> HttpResponse:
        assert_that(self.status_code).is_equal_to(expected_code)
        return self

    def json(self) -> Any:
        return self.wrapped_response.json()
