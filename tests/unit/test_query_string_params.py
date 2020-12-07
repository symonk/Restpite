from assertpy import assert_that

from restpite import Request


def test_query_string_params() -> None:
    example_params = {"one": "one", "two": "two", "three": "three"}
    assert_that(
        Request(url="http://www.google.com")
        .raise_on_failure()
        .retry(5)
        .with_query_params(example_params)
        .send()
        .status_code
    ).is_equal_to(200)
