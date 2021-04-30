from restpite import RespiteClient
from restpite import RestpiteResponse


class RestpiteRequest:
    ...

    def __call__(self, *args, **kwargs) -> RestpiteResponse:
        return self.send()

    def send(self) -> RestpiteResponse:
        with RespiteClient() as session:
            return session.get(
                **{k: v for k, v in self.__dict__.items() if k != "method"}
            )
