import pytest
import respx
from httpx import Response
from respx import Route

from restpite import RespiteClient

MOCK_URL = "https://www.google.com"


@respx.mock
@pytest.mark.parametrize("status_code", (100, 101, 102, 103))
def test_assert_informative(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_informative()
    assert route.called


# TODO => BUG! 207 compares 300 != 207 - why? weird..
@respx.mock
@pytest.mark.parametrize("status_code", (200, 201, 202, 203, 204, 205, 206, 208, 226))
def test_assert_successful(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_success()
    assert route.called


@respx.mock
@pytest.mark.parametrize("status_code", (300, 301, 302, 303, 304, 305, 307, 308))
def test_assert_redirect(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_redirect()
    assert route.called


CLIENT_ERRORS = (
    400,
    401,
    402,
    403,
    404,
    405,
    406,
    407,
    408,
    409,
    410,
    411,
    412,
    413,
    414,
    415,
    416,
    417,
    418,
    421,
    422,
    423,
    424,
    425,
    426,
    428,
    429,
    431,
    451,
)


@respx.mock
@pytest.mark.parametrize("status_code", CLIENT_ERRORS)
def test_assert_client_error(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_client_error()
    assert route.called


@respx.mock
@pytest.mark.parametrize(
    "status_code", (500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511)
)
def test_assert_server_error(status_code):
    route = _setup_route(status_code)
    RespiteClient().get(MOCK_URL).assert_server_error()
    assert route.called


def _setup_route(status_code: int) -> Route:
    return respx.get(MOCK_URL).mock(return_value=Response(status_code))
