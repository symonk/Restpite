from typing import Any
from typing import Callable

from assertpy import assert_that
from werkzeug.wrappers import Response

from restpite import HttpSession


def test_simple_session(local_http_server, random_headers_dict) -> None:
    call_back: Callable[[Any], Response] = lambda r: Response(
        "success", headers=dict(r.headers)
    )
    local_http_server.expect_request("/test").respond_with_handler(call_back)
    with HttpSession(headers=random_headers_dict) as session:
        response = session.http_get(f"http://localhost:{local_http_server.port}/test")
        assert_that(random_headers_dict).is_subset_of(response.headers)
