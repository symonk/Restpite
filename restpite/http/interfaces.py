import abc


class Mountable(abc.ABC):
    @abc.abstractmethod
    def mount(self) -> None:
        ...
