import abc


class AbstractHttpListener(abc.ABC):
    @abc.abstractmethod
    def before_send_request(self) -> None:
        pass

    @abc.abstractmethod
    def after_retrieve_response(self) -> None:
        pass

    @abc.abstractmethod
    def on_exception(self) -> None:
        pass
