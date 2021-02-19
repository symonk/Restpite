from restpite import HttpSession


def test_listener_hooks_are_called(local_http_server, sys_out_listener):
    local_http_server.expect_request("/")
    with HttpSession(listeners=[sys_out_listener]) as session:
        session.http_get(f"http://localhost:{local_http_server.port}/")
