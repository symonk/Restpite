import logging

from restpite import RestpiteResponse

log = logging.getLogger(__name__)


class RequestRecordingHandler:
    def __init__(self):
        ...

    def after_receiving_response(self, response: RestpiteResponse) -> None:
        # TODO: Jsonify response and write to file?
        log.warning(response.__dict__)
