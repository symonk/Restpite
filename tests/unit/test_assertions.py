import pytest
from _pytest.monkeypatch import MonkeyPatch
from httpx import Response

from restpite import RestpiteResponse
from restpite.exceptions.exceptions import RestpiteAssertionError
from restpite.http import status_code


def test_response_was_ok_status_code(monkeypatch: MonkeyPatch) -> None:
    r = Response(status_code=200)
    response = RestpiteResponse(r)
    response.assert_was_ok()


@pytest.mark.skip(reason="broken, fix it later")
def test_response_was_ok_failure(monkeypatch: MonkeyPatch) -> None:
    r = Response(status_code=201)
    response = RestpiteResponse(r)
    with pytest.raises(RestpiteAssertionError) as error:
        response.assert_was_ok()
    assert (
        error.value.message
        == "Http Response status code was: <201> not: <200> as expected"
    )


@pytest.mark.skip(reason="broken, fix it later")
@pytest.mark.parametrize("expected", ["GET", "PUT", "POST", "PATCH", "DELETE"])
def test_assert_request_type(monkeypatch: MonkeyPatch, expected) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.request_method", expected)
    monkeypatch.setattr(
        "restpite.http.status_code.StatusCode.from_code", status_code.CONTINUE
    )
    response = RestpiteResponse(Response())
    getattr(response, f"request_verb_was_{expected.lower()}")()
