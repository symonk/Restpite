from restpite import RespiteClient


def test_default_user_agent(respite_version) -> None:
    assert RespiteClient().headers.get("User-Agent") == respite_version


def test_custom_user_agent() -> None:
    expected = "expected"
    assert RespiteClient(user_agent=expected).headers.get("User-Agent") == expected
