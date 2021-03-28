import logging

from restpite import RestpiteListener
from restpite import RestpiteSession


def test_custom_listener_before_request(caplog):
    class BasicListener(RestpiteListener):
        def before_sending_request(self) -> None:
            logging.warning("Before sending request!")

    s = RestpiteSession(listeners=[BasicListener()])
    s.get("https://google.com")
    assert len(caplog.record_tuples) == 1
    assert ("root", 30, "Before sending request!") in caplog.record_tuples


def test_custom_listener_after_receiving_response(caplog):
    class BasicListener(RestpiteListener):
        def after_receiving_response(self, response) -> None:
            logging.warning(f"After sending response: {response}")

    s = RestpiteSession(listeners=[BasicListener()])
    s.get("https://google.com")
    assert len(caplog.record_tuples) == 1
    # TODO: Assert on repr of RestpiteResponse here later - needs implemented
