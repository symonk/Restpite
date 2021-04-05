import pytest
from _pytest.monkeypatch import MonkeyPatch
from requests import Response

from restpite import RestpiteResponse
from restpite.exceptions.exceptions import RestpiteAssertionError


def test_response_was_ok_status_code(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.status_code", 200)
    response = RestpiteResponse(Response())
    response.assert_was_ok()


def test_response_was_ok_failure(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("restpite.RestpiteResponse.status_code", 201)
    response = RestpiteResponse(Response())
    with pytest.raises(RestpiteAssertionError) as error:
        response.assert_was_ok()
    assert (
        error.value.message
        == "Http Response status code was: <201> not: <200> as expected"
    )
