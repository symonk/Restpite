import pytest

from tests.data_providers import data_service


@pytest.fixture
def random_headers_dict(data_provider):
    yield data_provider.lower_case_headers_of_len()


@pytest.fixture
def data_provider():
    yield data_service
