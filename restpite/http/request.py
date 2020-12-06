from typing import Dict


class Given:
    def __init__(self, url: str, q_string: Dict[str, str]):
        self.url = url
        self.q_string = self._build_url(q_string)

    def _build_url(self, params: Dict[str, str]) -> str:
        return f"{self.url}{''.join([])}"
