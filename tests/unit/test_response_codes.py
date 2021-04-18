import pytest
import respx
from httpx import Response
from respx import Route

from restpite import RespiteClient

MOCK_URL = "https://www.google.com"


@respx.mock
@pytest.mark.parametrize("status_code", (100, 199))
def test_assert_informative(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_informative()
    assert route.called


@respx.mock
@pytest.mark.parametrize("status_code", (200, 299))
def test_assert_successful(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_success()
    assert route.called


@respx.mock
@pytest.mark.parametrize("status_code", (300, 399))
def test_assert_redirect(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_redirect()
    assert route.called


@respx.mock
@pytest.mark.parametrize("status_code", (400, 499))
def test_assert_client_error(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_client_error()
    assert route.called


@respx.mock
@pytest.mark.parametrize("status_code", (500, 599))
def test_assert_server_error(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_server_error()
    assert route.called


def _setup_route(status_code: int) -> Route:
    return respx.get(MOCK_URL).mock(return_value=Response(status_code))
