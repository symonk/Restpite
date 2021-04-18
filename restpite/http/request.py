from restpite import RespiteClient
from restpite import RestpiteResponse


class RestpiteRequest:
    """
    The Entrypoint class to restpite.  Used for crafting custom requests (lazily)
    and later sending them.  The Request wrapper offers some in built testability.

    :param method: The HTTP Method this request will perform when sent.
    :param url: The request url
    :param params: Query string parameters to be appended to the url
    """

    def __init__(
        self,
        method: str,
        url: str,
        params=None,
        data=None,
        json=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=None,
        proxies=None,
        verify=None,
        stream=None,
        cert=None,
        enforce_success: bool = False,
    ) -> None:
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.json = json
        self.headers = headers
        self.cookies = cookies
        self.files = files
        self.auth = auth
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.proxies = proxies
        self.verify = verify
        self.stream = stream
        self.cert = cert
        self.enforce_success = enforce_success

    def __call__(self, *args, **kwargs) -> RestpiteResponse:
        return self.send()

    def send(self) -> RestpiteResponse:
        with RespiteClient() as session:
            return session.get(
                **{k: v for k, v in self.__dict__.items() if k != "method"}
            )
