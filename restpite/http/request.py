from restpite import RestpiteResponse
from restpite import RestpiteSession


class RestpiteRequest:
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

    def __call__(self, *args, **kwargs) -> RestpiteResponse:
        return self.send()

    def send(self) -> RestpiteResponse:
        with RestpiteSession() as session:
            return session.get(**self.__dict__)
