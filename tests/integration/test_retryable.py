import pytest
from assertpy import assert_that
from requests import RequestException
from requests.exceptions import RetryError

from restpite import RestpiteSession


def test_retryable_attempts_is_correct(
    local_http_server, httpserver_listen_address
) -> None:
    local_http_server.expect_request("/retries").respond_with_json(
        {"foo": "bar"}, status=404
    )
    with pytest.raises(RetryError):
        with RestpiteSession(retry=(3, 0.005, [404], RequestException)) as session:
            session.get(
                f"http://{local_http_server.host}:{local_http_server.port}/retries"
            )
    assert_that(len(local_http_server.log) == 4)
