from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Sequence
from typing import Type

from httpx import Response

from restpite.exceptions.exceptions import RestpiteAssertionError
from restpite.http import status_code
from restpite.http.schemas import RestpiteSchema
from restpite.protocols.restpite_protocols import Curlable


class RestpiteResponse(Curlable):
    def __init__(self, delegate: Response) -> None:
        self.delegate = delegate

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self.delegate, name)
        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)

        return wrapper

    def deserialize(
        self, schema: Type[RestpiteSchema], schema_kwargs: Dict[Any, Any]
    ) -> Any:
        # TODO: Incorporate schemas from marshmallow here to allow custom deserialization?
        # TODO: Small implementation; plenty of work still to do here!
        return schema(**schema_kwargs).load(self.delegate.json())

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
        if self.delegate.headers[header] != expected_value:
            message = f"Http Response header: {header} did not contain the value: {expected_value}"
            self.error(message)
        return self

    def assert_application_json(self) -> RestpiteResponse:
        """
        Scan the response object headers for the content-type header and assert that it contained
        application/json.  contains is used because it is not uncommon for this header to return
        charset utf-8; etc.
        """
        content_header = self.headers.get("Content-Type", None)
        if content_header is None:
            self.error(
                f"Response did not contain a `Content-Type` header.. {repr(self.headers)}"
            )
        if r"application/json" not in content_header:
            self.error(
                f"Response did not contain `application/json` in its content type header.. {repr(self.headers)}"
            )
        return self

    def assert_was_ok(self) -> RestpiteResponse:
        """

        """
        # TODO: Implement custom status codes to avoid indexing tuple sequences etc
        # TODO: https://github.com/symonk/restpite/issues/98
        if self.status_code != status_code.OK[0]:
            message = f"Http Response status code was: <{self.status_code}> not: <{status_code.OK[0]}> as expected"
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
        assert self.status_code == status_code.FORBIDDEN[0]
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
        assert len(self.delegate.history) == expected_length
        return self

    def had_status_code(self, expected_code: int) -> RestpiteResponse:
        assert self.status_code == expected_code
        return self

    def error(self, message: str) -> None:
        """
        Responsible for raising the `RestpiteAssertionError` which will subsequently cause tests
        to fail.  RestpiteAssertionError is a simple subclass of `AssertionError` with the aim
        in future to bolt on more functionality, currently it serves the same purpose.
        """
        raise RestpiteAssertionError(message) from None

    def curlify(self) -> str:
        raise NotImplementedError

    def __bool__(self) -> bool:
        """
        Permits truth checks on the HTTPResponse object, where it is considered
        True when the response was a successful response
        """
        self.assert_was_ok()
        return True
