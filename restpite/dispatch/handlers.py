import logging

from httpx import Request

from restpite.dispatch.dispatch_protocols import Notifyable

log = logging.getLogger(__name__)


class LoggingHandler(Notifyable):
    def before_sending_request(self, request: Request, **request_kw) -> None:
        log.debug(request)
        log.debug(request_kw)


BUILT_IN_HANDLERS = [LoggingHandler()]
