from typing import Mapping
from typing import Optional
from typing import Tuple


class RestpiteConfig:
    def __init__(
        self, default_headers: Optional[Tuple[str, Mapping[str, str]]]
    ) -> None:
        self.default_headers = default_headers
