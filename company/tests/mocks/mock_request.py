class MockRequest:
    def __init__(self, user=None, method="GET") -> None:
        self.user = user
        self.method = method
