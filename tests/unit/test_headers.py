from assertpy import assert_that

from restpite import HttpSession


def test_additional_headers(random_headers_dict) -> None:
    assert_that(
        HttpSession(headers=random_headers_dict).headers.items()
        < random_headers_dict.items()
    )


def test_default_headers_are_applied(request_default_headers) -> None:
    session = HttpSession()
    assert_that(session.headers).is_equal_to(request_default_headers)
