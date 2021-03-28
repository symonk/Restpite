import logging

import pytest

from restpite import RestpiteListener
from restpite import RestpiteSession

MOCK_URL = "http://test.com"


@pytest.mark.parametrize("codes", range(100, 200))
def test_assert_informative(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_informative()


@pytest.mark.parametrize("codes", range(200, 300))
def test_assert_successful(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_success()


@pytest.mark.parametrize("codes", range(300, 400))
def test_assert_redirect(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_redirect()


@pytest.mark.parametrize("codes", range(400, 500))
def test_assert_client_error(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_client_error()


@pytest.mark.parametrize("codes", range(500, 600))
def test_assert_server_error(requests_mock, codes):
    requests_mock.get(MOCK_URL, status_code=codes)
    RestpiteSession().get(MOCK_URL).assert_server_error()


def test_it(caplog):
    caplog.set_level(logging.INFO)

    class MyListener(RestpiteListener):
        def before_sending_request(self) -> None:
            logging.info("Sending my request!")

    with RestpiteSession(listeners=[MyListener()]) as s:
        s.get("https://www.google.com")
    assert caplog.records
