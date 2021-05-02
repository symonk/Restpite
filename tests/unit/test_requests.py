from restpite import http_get


def test_is_request_logged_by_builtins(caplog) -> None:
    http_get(url="https://www.google.com").send()
    # TODO: Finish!
