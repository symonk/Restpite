from assertpy import assert_that
from requests.utils import default_headers

from restpite import HttpSession
from restpite.http.headers import MergeHeaders
from restpite.http.headers import OnlyHeaders


def test_merge_headers_works_successfully(randomised_dict):
    with HttpSession(headers=MergeHeaders(randomised_dict)) as session:
        merged = {**default_headers(), **randomised_dict}
        assert_that(session.headers).is_equal_to(merged)


def test_only_headers_works_successfully(randomised_dict):
    with HttpSession(headers=OnlyHeaders(randomised_dict)) as session:
        assert_that(session.headers).is_equal_to(randomised_dict)


def test_without_headers_works_successfully():
    with HttpSession() as session:
        assert_that(session.headers).is_equal_to(default_headers())
