from restpite import RestpiteSession


def test_default_user_agent(respite_version) -> None:
    assert RestpiteSession().headers.get("User-Agent") == respite_version


def test_custom_user_agent() -> None:
    expected = "helloWorld"
    assert RestpiteSession(user_agent=expected).headers.get("User-Agent") == expected
