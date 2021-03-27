import logging

from .listener_protocols import RestpiteListener

log = logging.getLogger(__name__)


class LoggingListener(RestpiteListener):
    """
    A simple logging listener that writes logging information.
    """

    def before_sending_request(self) -> None:
        log.info("About to send a request")

    def after_receiving_response(self) -> None:
        log.info("Received a response!")

    def on_exception(self, exc: BaseException) -> None:
        log.info("Oh no an exception occurred!")
