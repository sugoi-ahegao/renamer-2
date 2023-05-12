import sys

from models.config import get_config


class StashLogger:
    def __init__(self, disable_logger: bool):
        self.disable_logger = disable_logger

    def _get_log_prefix(self, level_char):
        start_level_char = b"\x01"
        end_level_char = b"\x02"

        result = start_level_char + level_char + end_level_char
        return result.decode()

    def _log(self, level_char, msg):
        if self.disable_logger:
            return

        if level_char == "":
            raise ValueError("Level char cannot be empty")

        full_msg = self._get_log_prefix(level_char) + msg + "\n"
        print(full_msg, file=sys.stderr, flush=True)

    def trace(self, msg):
        self._log(b"t", msg)

    def debug(self, msg):
        self._log(b"d", msg)

    def info(self, msg):
        self._log(b"i", msg)

    def warn(self, msg):
        self._log(b"w", msg)

    def error(self, msg):
        self._log(b"e", msg)

    def progress(self, progress: float):
        if progress < 0 or progress > 1:
            raise ValueError("Progress must be between 0 and 1")

        self._log(b"p", str(progress))


def get_stash_logger():
    return StashLogger(disable_logger=False)
