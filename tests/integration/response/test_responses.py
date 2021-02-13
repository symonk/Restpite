from assertpy import assert_that
from requests import codes

from restpite import HttpSession

from tests.models.models import Car


def test_response_assert_ok(local_http_server) -> None:
    local_http_server.expect_request("/cars/bmw").respond_with_json(
        {"colour": "red", "brand": "bmw", "engine": 3200}, status=codes.ok
    )
    with HttpSession() as session:
        response = session.get(f"http://localhost:{local_http_server.port}/cars/bmw")
        response.assert_was_ok()
        assert_that(response.deserialize(Car)).is_instance_of(Car)
