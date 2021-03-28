import logging

from restpite import RestpiteListener
from restpite import RestpiteSession


def test_custom_listener_before_request(basic_endpoint_no_handler, caplog) -> None:
    class BasicListener(RestpiteListener):
        def before_sending_request(self) -> None:
            logging.warning("Before sending request!")

    s = RestpiteSession(listeners=[BasicListener()])
    s.get(basic_endpoint_no_handler)
    assert "Before sending request!" in caplog.text


def test_custom_listener_after_receiving_response(
    basic_endpoint_no_handler, caplog
) -> None:
    class BasicListener(RestpiteListener):
        def after_receiving_response(self, response) -> None:
            logging.warning(f"After sending response: {response}")

    s = RestpiteSession(listeners=[BasicListener()])
    s.get(basic_endpoint_no_handler)
    assert len(caplog.record_tuples) == 2
    # TODO: Account for werkzeug logging here...
    # TODO: Assert on repr of RestpiteResponse here later - needs implemented
