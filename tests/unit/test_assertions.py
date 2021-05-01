import pytest
from _pytest.monkeypatch import MonkeyPatch
from httpx import Response

from restpite import RestpiteResponse
from restpite.exceptions.exceptions import RestpiteAssertionError
from restpite.http.verb import DELETE
from restpite.http.verb import GET
from restpite.http.verb import PATCH
from restpite.http.verb import POST
from restpite.http.verb import PUT


def test_response_was_ok_status_code() -> None:
    response = RestpiteResponse(Response(status_code=200))
    response.assert_was_ok()


def test_response_was_ok_failure(monkeypatch: MonkeyPatch) -> None:
    response = RestpiteResponse(Response(status_code=201))
    with pytest.raises(RestpiteAssertionError) as error:
        response.assert_was_ok()
    assert (
        error.value.message
        == "Http Response status code was: <Response Code: <201, Created>> not: <200> as expected"
    )


@pytest.mark.parametrize("expected", [GET, PUT, POST, DELETE, PATCH])
def test_assert_request_type(monkeypatch: MonkeyPatch, expected) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.request_method", expected)
    response = RestpiteResponse(Response(status_code=100))
    getattr(response, f"request_verb_was_{expected.lower()}")()
