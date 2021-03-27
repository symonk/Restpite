import pytest
from requests.exceptions import RetryError

from restpite.http.session import RestpiteSession
from restpite.other.adapters import RetryAdapter


def test_retryable_get(local_http_server):
    local_http_server.expect_request("/retry").respond_with_json("", status=500)
    adapter = RetryAdapter(
        "http://", until_status_in=200, max_attempts=2, backoff_factor=0.01
    )
    with RestpiteSession(adapters=[adapter]) as s:
        with pytest.raises(RetryError):
            s.http_get(f"http://localhost:{local_http_server.port}/retry")
