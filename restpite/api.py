"""
This module implements the Restpite api

:copyright: (c) 2020 by Simon Kerr.
:license: MIT, see LICENSE for more details.
"""

from restpite import RestpiteRequest
from restpite import RestpiteResponse
from restpite import RestpiteSession


def request(method: str, url: str, **kwargs) -> RestpiteResponse:
    with RestpiteSession() as session:
        return session.get(method, url, **kwargs)


def get(url: str, **kwargs) -> RestpiteResponse:
    """
    Constructs and sends a :class:`RespiteRequest`
    :param url: str
    """
    return RestpiteRequest(method="get", url=url, **kwargs).send()
