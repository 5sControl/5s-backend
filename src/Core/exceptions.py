class SenderError(Exception):
    def __init__(self, path):
        self.path = path
        super().__init__(f"Error creating camera. Path: {path}")


class InvalidResponseError(Exception):
    def __init__(self, path, status):
        self.path = path
        self.status = status
        super().__init__(f"Invalid response. Path: {path}, status: {status}")
