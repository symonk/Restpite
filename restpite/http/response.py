from __future__ import annotations

import functools
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import Sequence
from typing import Type

from httpx import Response

from restpite.constants.response_assertion_templates import REQUEST_VERB_MISMATCH
from restpite.constants.response_assertion_templates import RESPONSE_NO_HEADER
from restpite.constants.response_assertion_templates import RESPONSE_STATUS_CODE_MISMATCH
from restpite.exceptions.exceptions import RestpiteAssertionError
from restpite.http.schemas import RestpiteSchema
from restpite.http.status_code import StatusCode
from restpite.http.verb import CONNECT
from restpite.http.verb import DELETE
from restpite.http.verb import GET
from restpite.http.verb import HEAD
from restpite.http.verb import OPTIONS
from restpite.http.verb import PATCH
from restpite.http.verb import POST
from restpite.http.verb import PUT
from restpite.http.verb import TRACE
from restpite.protocols.restpite_protocols import Curlable


class RestpiteResponse(Curlable):
    def __init__(self, delegate: Response) -> None:
        self.delegate = delegate
        self.status_code = StatusCode.from_code(self.delegate.status_code)

    @property
    def request_method(self) -> AnyStr:
        return self.delegate.request.method  # type: ignore

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self.delegate, name)
        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)

        return wrapper

    def deserialize(self, schema: Type[RestpiteSchema], schema_kwargs: Dict[Any, Any]) -> Any:
        # TODO: Incorporate schemas from marshmallow here to allow custom deserialization?
        # TODO: Small implementation; plenty of work still to do here!
        return schema(**schema_kwargs).load(self.delegate.json())

    # -------------------------------- HTTP RESPONSE STATUS CODE ASSERTIONS --------------------------------

    def had_informative_status_code(self) -> RestpiteResponse:
        """
        Enforces that the response status code was a 1xx (Informational) based code.  Note we do a wide assertion of
        100-199 but often these are limited to a very small subset of that range, should this change in future
        restpite will just work.
        """
        self._assert_response_code_in_range(range(100, 200))
        return self

    def had_success_status_code(self) -> RestpiteResponse:
        """
        Enforces that the response status code was a 2xx (Successful) based code.  Note we do a wide assertion of
        200-299 but often these are limited to a very small subset of that range, should this change in future
        restpite will just work.
        """
        self._assert_response_code_in_range(range(200, 300))
        return self

    def had_redirect_status_code(self) -> RestpiteResponse:
        """
        Enforces that the response status code was a 3xx (Redirection) based code.  Note we do a wide assertion of
        300-399 but often these are limited to a very small subset of that range, should this change in future
        restpite will just work.
        """
        self._assert_response_code_in_range(range(300, 400))
        return self

    def had_client_error_status_code(self) -> RestpiteResponse:
        """
        Enforces that the response status code was a 4xx (Client Error) based code.  Note we do a wide assertion of
        400-499 but often these are limited to a very small subset of that range, should this change in future
        restpite will just work.
        """
        self._assert_response_code_in_range(range(400, 500))
        return self

    def had_server_error_status_code(self) -> RestpiteResponse:
        """
        Enforces that the response status code was a 3xx (Server Error) based code.  Note we do a wide assertion of
        500-599 but often these are limited to a very small subset of that range, should this change in future
        restpite will just work.
        """
        self._assert_response_code_in_range(range(500, 600))
        return self

    def had_status(self, expected_code: int) -> RestpiteResponse:
        """
        Given a status code, matches the response against it.
        :param expected_code: The expected status code, it is the callers responsibility here
        to provide a 3 digit status code.
        """
        if expected_code != self.status_code.code:
            self.raise_assert_failure(RESPONSE_STATUS_CODE_MISMATCH.format(self.status_code, expected_code))
        return self

    def _assert_response_code_in_range(self, expected_range: Sequence[int]) -> None:
        """
        Validates the wrapped response object had a status code inside a particular range
        :param expected_range: A sequence of integers to check the status code is in
        :raises RestpiteAssertionError: If the status code is not in expected_range
        """
        if self.status_code.code not in expected_range:
            self.raise_assert_failure(f"Expected: {self.status_code} to be in: {expected_range} but it was not")

    # -------------------------------- HTTP RESPONSE HEADER ASSERTIONS -------------------------------------

    def had_header(self, header: str) -> RestpiteResponse:
        """
        Checks the response HTTP headers for a match based on the HTTP header name.  As per RFC 7231
        HTTP header fields should be case-insensitive, by default the header instance here is a
        case insensitive dictionary to cater to that.

        :param header: The header name to lookup in the response HTTP headers
        """
        if header not in self.headers:
            self.raise_assert_failure(RESPONSE_NO_HEADER.format(header))
        return self

    # -------------------------------- HTTP REQUEST RELATED ASSERTIONS -------------------------------------

    def request_verb_was(self, expected_method: str) -> RestpiteResponse:
        """
        Checks the request HTTP method type that was initially sent to the server.  These have relatively
        simple use, as it would be rare to assert on a request that the client crafted.

        :param expected_method: The HTTP Verb (string) that the request method should be
        """
        if self.request_method != expected_method.upper():
            self.raise_assert_failure(REQUEST_VERB_MISMATCH.format(self.request_method, expected_method))
        return self

    request_verb_was_connect = functools.partialmethod(request_verb_was, CONNECT)
    request_verb_was_delete = functools.partialmethod(request_verb_was, DELETE)
    request_verb_was_get = functools.partialmethod(request_verb_was, GET)
    request_verb_was_head = functools.partialmethod(request_verb_was, HEAD)
    request_verb_was_options = functools.partialmethod(request_verb_was, OPTIONS)
    request_verb_was_patch = functools.partialmethod(request_verb_was, PATCH)
    request_verb_was_post = functools.partialmethod(request_verb_was, POST)
    request_verb_was_put = functools.partialmethod(request_verb_was, PUT)
    request_verb_was_trace = functools.partialmethod(request_verb_was, TRACE)

    # ------------------------------------------------------------------------------------------------------

    def raise_assert_failure(self, message: str) -> None:
        """
        Responsible for raising the `RestpiteAssertionError` which will subsequently cause tests
        to fail.  RestpiteAssertionError is a simple subclass of `AssertionError` with the aim
        in future to bolt on more functionality, currently it serves the same purpose.
        """
        raise RestpiteAssertionError(message) from None

    def curlify(self) -> str:
        # TODO: Debatable functionality
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO: Debatable implementation!
        return f"<[{repr(self.status_code)} : {self.delegate.url}]>"
