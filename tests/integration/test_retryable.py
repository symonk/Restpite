import pytest

from restpite import RestpiteSession


@pytest.mark.skip(reason="wip")
def test_retryable_attempts_is_correct(
    local_http_server, httpserver_listen_address
) -> None:
    local_http_server.expect_request("/retries").respond_with_json({"foo": "bar"})
    with RestpiteSession() as session:
        session.get(
            f"https://{local_http_server.host}:{local_http_server.port}/retries"
        )
