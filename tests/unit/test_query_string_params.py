from assertpy import assert_that
from requests import RequestException

from restpite import Request


def test_query_string_params() -> None:
    example_params = {"one": "one", "two": "two", "three": "three"}
    assert_that(
        Request(
            url="http://www.google.com",
            query_params=example_params,
            raise_on_failure=True,
            retryable=(5, RequestException),
        )
        .get()
        .status_code
    ).is_equal_to(200)
