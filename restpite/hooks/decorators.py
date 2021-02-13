from restpite import HttpResponse
from restpite import Request


def pre_send(request: Request):
    pass


def post_send(request: Request):
    pass


def pre_receive(response: HttpResponse):
    pass


def post_receive(response: HttpResponse):
    pass
