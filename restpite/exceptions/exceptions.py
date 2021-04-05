class RestpiteAssertionError(AssertionError):
    def __init__(self, message: str) -> None:
        self.message = message
