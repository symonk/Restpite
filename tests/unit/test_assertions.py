import pytest
from _pytest.monkeypatch import MonkeyPatch
from requests import Response

from restpite import RestpiteResponse
from restpite.exceptions.exceptions import RestpiteAssertionError


def test_response_was_ok_status_code(monkeypatch: MonkeyPatch) -> None:
    r = Response()
    r.status_code = 200
    response = RestpiteResponse(r)
    response.assert_was_ok()


def test_response_was_ok_failure(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.status_code", 201, raising=False)
    response = RestpiteResponse(Response())
    with pytest.raises(RestpiteAssertionError) as error:
        response.assert_was_ok()
    assert (
        error.value.message
        == "Http Response status code was: <201> not: <200> as expected"
    )


@pytest.mark.parametrize("expected", ["GET", "PUT", "POST", "PATCH", "DELETE"])
def test_assert_request_type(monkeypatch: MonkeyPatch, expected) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.request_method", expected)
    response = RestpiteResponse(Response())
    getattr(response, f"request_verb_was_{expected.lower()}")()
