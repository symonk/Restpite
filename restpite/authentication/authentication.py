class Auth:
    ...


class NoAuth:
    def __call__(self, *args, **kwargs) -> None:
        ...
