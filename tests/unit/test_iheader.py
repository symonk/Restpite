from assertpy import assert_that
from requests.utils import default_headers

from restpite import HttpSession
from restpite.http.headers import MergeHeaders
from restpite.http.headers import OnlyHeaders


def test_merge_headers_works_successfully(random_headers_dict):
    with HttpSession(headers=MergeHeaders(random_headers_dict)) as session:
        merged = {**default_headers(), **random_headers_dict}
        assert_that(session.headers).is_equal_to(merged)


def test_only_headers_works_successfully(random_headers_dict):
    with HttpSession(headers=OnlyHeaders(random_headers_dict)) as session:
        assert_that(session.headers).is_equal_to(random_headers_dict)


def test_without_headers_works_successfully():
    with HttpSession() as session:
        assert_that(session.headers).is_equal_to(default_headers())
