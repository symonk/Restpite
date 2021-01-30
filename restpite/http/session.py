from __future__ import annotations

from typing import Optional

from requests import Session

from restpite.http.headers import IHeader


class HttpSession(Session):
    def __init__(self, headers: Optional[IHeader] = None):
        super().__init__()
        if headers:
            self.headers = headers.resolve_headers(self.headers)
