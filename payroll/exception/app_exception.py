from typing import List
from .error_message import BaseMessage


class AppException(Exception):
    def __init__(self, error_message: BaseMessage, details: str | List[str] = None):
        self.code = error_message.code
        self.text = error_message.format_message(details)
        self.http_status = error_message.http_status
