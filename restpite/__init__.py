"""isort:skip_file"""

import importlib.metadata

__version__ = importlib.metadata.version("restpite")

from .http import status_code
from .http.response import RestpiteResponse
from .dispatch.dispatch_protocols import Notifyable
from .http.client import RespiteClient
from .http.request import RestpiteRequest
from .http.request import http_connect
from .http.request import http_delete
from .http.request import http_get
from .http.request import http_patch
from .http.request import http_put
from .http.request import http_post
from .http.request import http_head
from .http.request import http_options
from .http.request import http_trace


import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__all__ = [
    "RespiteClient",
    "RestpiteRequest",
    "RestpiteResponse",
    "Notifyable",
    "status_code",
    "http_options",
    "http_trace",
    "http_head",
    "http_put",
    "http_connect",
    "http_delete",
    "http_post",
    "http_get",
    "http_patch",
    "__version__",
]
