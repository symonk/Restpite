from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Sequence
from typing import Type

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

    def assert_header_matches(
        self, header: str, expected_value: str
    ) -> RestpiteResponse:
        if self.wrapped_response.headers[header] != expected_value:
            message = f"Http Response header: {header} did not contain the value: {expected_value}"
            self.error(message)
        return self

    def assert_was_ok(self) -> RestpiteResponse:
        """

        """
        if self.status_code != status_codes.ok:
            message = f"Http Response status code was: <{self.status_code}> not: <{status_codes.ok}> as expected"
            self.error(message)
        return self

    def assert_informative(self) -> RestpiteResponse:
        """
        Validates the response status code was in the informative range.
        This is all status codes starting with: 1xx
        :raises RestpiteAssertionError: If the status code is outside the permitted range
        """
        self._assert_response_code_in_range(range(100, 200))
        return self

    def assert_success(self) -> RestpiteResponse:
        """
        Validates the response status code was in the successful range.
        This is all status codes starting with: 2xx
        :raises RestpiteAssertionError: If the status code is outside the permitted range
        """
        self._assert_response_code_in_range(range(200, 300))
        return self

    def assert_redirect(self) -> RestpiteResponse:
        """
        Validates the response status code was in the redirect range.
        This is all status codes starting with: 3xx
        :raises RestpiteAssertionError: If the status code is outside the permitted range
        """
        self._assert_response_code_in_range(range(300, 400))
        return self

    def assert_client_error(self) -> RestpiteResponse:
        """
        Validates the response status code was in the client error range.
        This is all status codes starting with: 4xx
        :raises RestpiteAssertionError: If the status code is outside the permitted range
        """
        self._assert_response_code_in_range(range(400, 500))
        return self

    def assert_server_error(self) -> RestpiteResponse:
        """
        Validates the response status code was in the server error range.
        This is all status codes starting with: 5xx
        :raises RestpiteAssertionError: If the status code is outside the permitted range
        """
        self._assert_response_code_in_range(range(500, 600))
        return self

    def assert_was_forbidden(self) -> RestpiteResponse:
        assert self.status_code == status_codes.forbidden
        return self

    def _assert_response_code_in_range(self, expected_range: Sequence[int]) -> None:
        """
        Validates the wrapped response object had a status code inside a particular range
        :param expected_range: A sequence of integers to check the status code is in
        :raises RestpiteAssertionError: If the status code is not in expected_range
        """
        if self.status_code not in expected_range:
            self.error(
                f"Expected: {self.status_code} to be in: {expected_range} but it was not"
            )

    def history_length_was(self, expected_length: int) -> RestpiteResponse:
        assert len(self.wrapped_response.history) == expected_length
        return self

    def had_status_code(self, expected_code: int) -> RestpiteResponse:
        assert self.status_code == expected_code
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
