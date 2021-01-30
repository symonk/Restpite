import abc
import functools

from requests import Response


class Writable(abc.ABC):
    @abc.abstractmethod
    def record(self, response: Response) -> None:
        pass


class JsonWritable(Writable):
    def record(self, response: Response) -> None:
        pass


def record(f):
    @functools.wraps(f)
    def record_inner(*args, **kwargs):
        writer = JsonWritable()
        response = f(*args, **kwargs)
        writer.record(response)
        return response

    return record_inner
