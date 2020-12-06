import pytest


@pytest.fixture(scope="session", autouse=True)
def local_http_server():
    ...
