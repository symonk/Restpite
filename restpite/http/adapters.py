import abc


class Mountable(abc.ABC):
    def __init__(self, prefix: str, adapter):
        self.prefix = prefix
        self.adapter = adapter

    def __iter__(self):
        return iter((self.prefix, self.adapter))


class Retryable(Mountable):
    ...
