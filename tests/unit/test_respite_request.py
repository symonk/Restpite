from restpite.http.request import http_get


def test_respite_request() -> None:
    req = http_get(url="https://www.google.com").send()
    req.assert_was_ok()
