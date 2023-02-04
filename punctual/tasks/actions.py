import logging

from pathlib import Path

logger = logging.getLogger(__name__)


class Action(object):
    def __init__(self, name: str,  path: str):
        self.name = name
        self.path = path

    def produce_action(self):
        file_path = str(Path(self.path))
        popen_args = ['python', file_path]
        logger.debug(f"Executing {file_path}")
        print(f"Executing {file_path}")

        return popen_args

