from assertpy import assert_that

from restpite import RestpiteSession


def test_additional_headers(random_headers_dict) -> None:
    assert_that(
        RestpiteSession(headers=random_headers_dict).headers.items()
        < random_headers_dict.items()
    )


def test_default_user_agent(respite_version) -> None:
    assert_that(RestpiteSession().headers.get("User-Agent")).is_equal_to(
        respite_version
    )


def test_custom_user_agent() -> None:
    expected = "helloWorld"
    assert_that(
        RestpiteSession(user_agent=expected).headers.get("User-Agent")
    ).is_equal_to(expected)
