import pytest


@pytest.fixture(scope="function")
def local_http_server(httpserver):
    # Gain more control around this fixture later
    print(f"Mock server: http://localhost:{httpserver.port}")
    yield httpserver
