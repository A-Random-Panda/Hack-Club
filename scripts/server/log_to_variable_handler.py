'''This module includes a handler that puts the latest log into a variable'''

import logging
from typing import override
from collections import deque

class LatestLogHandler(logging.Handler):
    '''Handler that puts the latest log into a variable'''
    MAX_LOGS:int = 30
    latest_logs:deque[str] = deque()

    @classmethod
    def save_log(cls, formatted_record: str) -> None:
        '''Saves the log of the message'''
        if len(cls.latest_logs) >= cls.MAX_LOGS:
            cls.latest_logs.popleft()
        cls.latest_logs.append(formatted_record)

    @classmethod
    def get_logs(cls) -> str:
        '''Returns the last MAX_LOGS logs'''
        return "\n".join(cls.latest_logs)

    @override
    def emit(self, record: logging.LogRecord) -> None:
        self.save_log(self.format(record))
