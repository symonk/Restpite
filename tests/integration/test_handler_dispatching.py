import logging

from restpite import Notifyable
from restpite import RestpiteSession


def test_custom_handler_before_request(basic_endpoint_no_handler, caplog) -> None:
    class BasicHandler(Notifyable):
        def before_sending_request(self) -> None:
            logging.warning("Before sending request!")

    s = RestpiteSession(handlers=[BasicHandler()])
    s.get(basic_endpoint_no_handler)
    assert "Before sending request!" in caplog.text


def test_custom_handler_after_receiving_response(
    basic_endpoint_no_handler, caplog
) -> None:
    class BasicHandler(Notifyable):
        def after_receiving_response(self, response) -> None:
            logging.warning(f"After sending response: {response}")

    s = RestpiteSession(handlers=[BasicHandler()])
    s.get(basic_endpoint_no_handler)
    assert len(caplog.record_tuples) == 2
    # TODO: Account for werkzeug logging here...
    # TODO: Assert on repr of RestpiteResponse here later - needs implemented
