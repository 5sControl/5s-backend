class SenderError(Exception):
    def __init__(self, path):
        self.path = path
        super().__init__(f"Error creating camera. Path: {path}")


class InvalidResponseError(Exception):
    def __init__(self, path, status):
        self.path = path
        self.status = status
        super().__init__(f"Invalid response. Path: {path}, status: {status}")


class DatabaseConnectioneError(Exception):
    def __init__(self, func_name):
        self.func_name = func_name
        super().__init__(f"Database connection error. Function: {func_name}")


class CameraConnectionError(Exception):
    def __class__(self, camera_ip):
        self.camera_ip = camera_ip
        super().__init__(f"Camera {camera_ip} connection error")
