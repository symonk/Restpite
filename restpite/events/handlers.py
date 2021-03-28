import logging

from restpite import RestpiteResponse

from .event_protocols import NotifyProtocol

log = logging.getLogger(__name__)


class RequestRecordingHandler(NotifyProtocol):
    def __init__(self):
        ...

    def after_receiving_response(self, response: RestpiteResponse) -> None:
        # TODO: Jsonify response and write to file?
        log.warning(response.__dict__)
