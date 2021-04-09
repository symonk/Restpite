import pytest
from pytest_mock import MockerFixture

from restpite.dispatch.dispatcher import HandlerDispatcher
from restpite.http.response import RestpiteResponse


class SpyHandler:
    def before_sending_request(self) -> None:
        ...

    def after_receiving_response(self, response: RestpiteResponse) -> None:
        ...

    def on_exception(self, exc: BaseException) -> None:
        ...


def test_handler_teardown(mocker: MockerFixture) -> None:
    dispatcher = HandlerDispatcher()
    handler = SpyHandler()
    spy = mocker.spy(dispatcher, "subscribe")
    dispatcher.subscribe(handler)
    spy.assert_called_once_with(handler)


def test_raises_on_no_protocol() -> None:
    with pytest.raises(TypeError) as error:
        handler = HandlerDispatcher()
        handler.subscribe(1337)
    assert (
        error.value.args[0]
        == "Type of handle was: <class 'int'>, it should be: <class 'typing._ProtocolMeta'>"
    )
