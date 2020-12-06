from typing import Dict
from typing import Optional
from urllib.parse import urlencode


class Given:
    def __init__(self, url: str, q_string: Dict[str, str]):
        self.q_string = q_string
        self.url = self._build_url(url, q_string)

    @staticmethod
    def _build_url(url: str, params: Optional[Dict[str, str]] = None) -> str:
        """
        Encode query string params dictionary and append it to the URL.
        :param params: Dictionary of k:v pairs to url encode and append to the url.
        :returns: Resolved url including query string params.
        """
        return url if not params else f"{url}?{urlencode(params)}"
