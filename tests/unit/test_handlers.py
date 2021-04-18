from _pytest.monkeypatch import MonkeyPatch

from restpite import RespiteClient


class BasicHandler:
    def before_sending_request(self) -> None:
        ...

    def after_receiving_response(self) -> None:
        ...

    def on_exception(self) -> None:
        ...


# TODO: Spy on handler calls to ensure Restpite is invoking them!


def test_before_sending_request(monkeypatch: MonkeyPatch) -> None:
    handler = BasicHandler()
    response = RespiteClient(handlers=[handler])  # noqa
    ...


def test_after_receiving_response():
    ...


def test_on_exception_handler():
    ...
