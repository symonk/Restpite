from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Type

from assertpy import assert_that
from requests import Response
from requests import codes as status_codes
from requests.utils import CaseInsensitiveDict

from restpite.exceptions.exceptions import RestpiteAssertionError


class RestpiteResponse:
    def __init__(self, wrapped_response: Response) -> None:
        self.wrapped_response = wrapped_response
        self.model: Optional[Any] = None

    @property
    def status_code(self) -> int:
        return self.wrapped_response.status_code

    @property
    def headers(self) -> CaseInsensitiveDict[Any]:
        return self.wrapped_response.headers

    def deserialize(self, model: Type[Any], *args, **kwargs) -> Any:
        # TODO: Incorporate schemas from marshmallow here to allow custom deserialization?
        return model(**self.wrapped_response.json())

    def assert_contained_header(self, header_name: str) -> RestpiteResponse:
        """
        Given a header name (key), enforces that the HTTP response headers dictionary
        contained a HTTP Header under such key.
        :param header_name: A string to lookup in the http response headers mapping
        """
        if header_name not in self.headers:
            message = f"Http Response did not contain a header known as {header_name}"
            self.error(message)
        return self

    def assert_value_was(self, header: str, expected_value: str) -> RestpiteResponse:
        assert_that(self.headers.get(header)).is_equal_to(expected_value)
        return self

    def assert_was_ok(self) -> RestpiteResponse:
        """

        """
        if self.status_code != status_codes.ok:
            message = f"Http Response status code was: <{self.status_code}> not: <{status_codes.ok}> as expected"
            self.error(message)
        return self

    def assert_informative(self) -> RestpiteResponse:
        assert_that(self.status_code).is_between(100, 199)
        return self

    def assert_success(self) -> RestpiteResponse:
        assert_that(self.status_code).is_between(200, 299)
        return self

    def assert_redirect(self) -> RestpiteResponse:
        assert_that(self.status_code).is_between(300, 399)
        return self

    def assert_client_error(self) -> RestpiteResponse:
        assert_that(self.status_code).is_between(400, 499)
        return self

    def assert_server_error(self) -> RestpiteResponse:
        assert_that(self.status_code).is_between(500, 599)
        return self

    def assert_was_forbidden(self) -> RestpiteResponse:
        assert_that(self.status_code).is_equal_to(status_codes.forbidden)
        return self

    def history_length_was(self, expected_length: int) -> RestpiteResponse:
        assert_that(self.wrapped_response.history).is_length(expected_length)
        return self

    def had_status_code(self, expected_code: int) -> RestpiteResponse:
        assert_that(self.status_code).is_equal_to(expected_code)
        return self

    def json(self) -> Any:
        return self.wrapped_response.json()

    def error(self, message: str) -> None:
        """
        Responsible for raising the `RestpiteAssertionError` which will subsequently cause tests
        to fail.  RestpiteAssertionError is a simple subclass of `AssertionError` which the aim
        in future to bolt on more functionality, currently it serves the same purpose.
        """
        raise RestpiteAssertionError(message) from None

    def __bool__(self) -> bool:
        """
        Permits truth checks on the HTTPResponse object, where it is considered
        True when the response was a successful response
        """
        return self.wrapped_response.ok
