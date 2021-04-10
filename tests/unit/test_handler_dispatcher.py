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
    spy = mocker.spy(handler, "on_exception")
    dispatcher.subscribe(handler)
    exc = Exception("foobar")
    dispatcher.dispatch("on_exception", exc)
    spy.assert_called_once_with(exc)


def test_lifo_handler_dispatching() -> None:
    # TODO: Implement!
    ...


def test_raises_on_no_protocol() -> None:
    with pytest.raises(TypeError) as error:
        handler = HandlerDispatcher()
        handler.subscribe(1337)  # noqa
    assert (
        error.value.args[0]
        == "Type of handle was: <class 'int'>, it should be: <class 'typing._ProtocolMeta'>"
    )


def test_dispatch_handler_resetting():
    dispatcher = HandlerDispatcher()
    dispatcher.subscribe(SpyHandler())
    assert len(dispatcher.handlers) == 1
    dispatcher.reset()
    assert len(dispatcher.handlers) == 0
