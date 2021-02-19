import pytest

from restpite import HttpSession

MOCK_URL = "http://test.com"


@pytest.mark.parametrize("codes", range(100, 200))
def test_assert_informative(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    with HttpSession() as session:
        session.http_get(MOCK_URL).assert_informative()


@pytest.mark.parametrize("codes", range(200, 300))
def test_assert_successful(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    with HttpSession() as session:
        session.http_get(MOCK_URL).assert_success()


@pytest.mark.parametrize("codes", range(300, 400))
def test_assert_redirect(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    with HttpSession() as session:
        session.http_get(MOCK_URL).assert_redirect()


@pytest.mark.parametrize("codes", range(400, 500))
def test_assert_client_error(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    with HttpSession() as session:
        session.http_get(MOCK_URL).assert_client_error()


@pytest.mark.parametrize("codes", range(500, 600))
def test_assert_server_error(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    with HttpSession() as session:
        session.http_get(MOCK_URL).assert_server_error()
