import pytest


@pytest.fixture
def basic_endpoint_no_handler(httpserver):
    return f"http://{httpserver.host}:{httpserver.port}"
