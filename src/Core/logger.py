import os
import logging


class Logger:
    def __init__(self, name, level=logging.DEBUG, filename="log"):
        self.name = name
        self.level = level
        self.filename = filename
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.file_handler = logging.FileHandler(
            os.path.join(os.getcwd(), f"{self.filename}.log")
        )
        self.file_handler.setLevel(self.level)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def debug(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.warning(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


logger = Logger("5SControl")
