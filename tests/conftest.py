import pytest
import requests

from restpite import HttpResponse
from restpite.listeners.interface import RestpiteListener

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
def sys_out_listener():
    class SysOutListener(RestpiteListener):
        def before_sending_request(self, *args, **kwargs) -> None:
            print(*args, **kwargs)

        def after_receiving_response(self, response: HttpResponse) -> None:
            print(response)

        def on_exception(self, exc) -> None:
            print(exc)

    return SysOutListener()
