import pytest
import requests

from tests.data_providers import data_service


@pytest.fixture
def random_headers_dict(data_provider):
    yield data_provider.lower_case_headers_of_len()


@pytest.fixture
def data_provider():
    yield data_service


@pytest.fixture
def request_default_headers():
    return requests.utils.default_headers()


@pytest.fixture
def respite_version() -> str:
    from restpite import __version__

    return f"restpite-{__version__}"
