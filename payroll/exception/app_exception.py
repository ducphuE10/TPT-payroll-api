from .error_message import BaseMessage


class AppException(Exception):
    def __init__(self, error_message: BaseMessage):
        self.code = error_message.code
        self.text = error_message.text
