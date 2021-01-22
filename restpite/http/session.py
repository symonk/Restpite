from typing import Optional

from ..configuration.config import Configuration


class Session:
    def __init__(self, session_configuration: Optional[Configuration] = None) -> None:
        self.session_configuration = session_configuration or Configuration()
