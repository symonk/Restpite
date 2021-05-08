import pytest
from _pytest.monkeypatch import MonkeyPatch
from httpx import Response

from restpite import RestpiteResponse
from restpite.exceptions.exceptions import RestpiteAssertionError
from restpite.http.verb import CONNECT
from restpite.http.verb import DELETE
from restpite.http.verb import GET
from restpite.http.verb import HEAD
from restpite.http.verb import OPTIONS
from restpite.http.verb import PATCH
from restpite.http.verb import POST
from restpite.http.verb import PUT
from restpite.http.verb import TRACE


def test_response_was_ok_status_code() -> None:
    response = RestpiteResponse(Response(status_code=200))
    response.had_status(200)


def test_response_was_ok_failure(monkeypatch: MonkeyPatch) -> None:
    response = RestpiteResponse(Response(status_code=201))
    with pytest.raises(RestpiteAssertionError) as error:
        response.had_status(200)
    assert error.value.message == "Http Response status code: Response Code: <201, Created>, was not: 200"


def test_assert_verb_was(monkeypatch) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.request_method", "GET")
    response = RestpiteResponse(Response(status_code=100))
    response.request_verb_was("GET")


@pytest.mark.parametrize("expected", [CONNECT, DELETE, GET, HEAD, OPTIONS, PUT, POST, PATCH, TRACE])
def test_assert_request_type(monkeypatch: MonkeyPatch, expected) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.request_method", expected)
    response = RestpiteResponse(Response(status_code=100))
    method = getattr(response, f"request_verb_was_{expected.lower()}")
    method()
