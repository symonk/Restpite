import pytest

from restpite import RestpiteSession

MOCK_URL = "http://test.com"


@pytest.mark.parametrize("codes", (100, 199))
def test_assert_informative(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_informative()


@pytest.mark.parametrize("codes", (200, 299))
def test_assert_successful(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_success()


@pytest.mark.parametrize("codes", (300, 399))
def test_assert_redirect(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_redirect()


@pytest.mark.parametrize("codes", (400, 499))
def test_assert_client_error(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_client_error()


@pytest.mark.parametrize("codes", (500, 599))
def test_assert_server_error(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_server_error()
