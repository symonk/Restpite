class AbstractHttpListener:
    """
    Custom listeners must subclass and partially or fully implement this interface
    """

    def before_sending_request(self) -> None:
        ...

    def after_receiving_response(self) -> None:
        ...

    def on_exception(self, exc: BaseException) -> None:
        ...
