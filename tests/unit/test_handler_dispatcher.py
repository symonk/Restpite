from pytest_mock import MockerFixture

from restpite.dispatch.dispatcher import HandlerDispatcher
from restpite.http.response import RestpiteResponse
from restpite.protocols.restpite_protocols import Notifyable


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


def test_handlers_fail_to_store_non_notifyable() -> None:
    handler = HandlerDispatcher()
    handler.subscribe(None)
    assert not handler._handlers


def test_handlers_register() -> None:
    handler = HandlerDispatcher()

    class Klazz(Notifyable):
        ...

    klazz = Klazz()
    handler.subscribe(klazz)
    assert len(handler._handlers) == 1 and handler._handlers[0] == klazz


def test_dispatch_handler_resetting():
    dispatcher = HandlerDispatcher()
    dispatcher.subscribe(SpyHandler())
    assert len(dispatcher._handlers) == 1
    dispatcher.reset()
    assert len(dispatcher._handlers) == 0
