import abc

from restpite.http.response import HttpResponse


class AbstractHttpListener(abc.ABC):
    @abc.abstractmethod
    def before_send_request(self) -> None:
        pass

    @abc.abstractmethod
    def after_retrieve_response(self, response: HttpResponse) -> None:
        pass

    @abc.abstractmethod
    def on_exception(self, exc: BaseException) -> None:
        pass
