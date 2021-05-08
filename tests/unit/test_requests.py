from restpite import RespiteClient
from restpite import http_get


def test_is_request_logged_by_builtins(caplog) -> None:
    http_get(url="https://www.google.com").send()
    # TODO: Finish!


async def test_async_client() -> None:
    async with RespiteClient() as c:
        c.get("https://www.google.com")
