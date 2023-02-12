import logging

from pathlib import Path

logger = logging.getLogger(__name__)


class Action(object):
    def __init__(self, name: str,  path: str, action_type: str, args: any = None):
        self.name = name
        self.path = path
        self.action_type = action_type
        self.args = args
        self.action_types = {
            "python": {
                "exe": "python.exe",
                "args": ""
            },
            "powershell": {
                "exe": "powershell.exe",
                "args": "-nologo -windowstyle hidden -ex bypass -file"
            },
            "exe": {
                "exe": "",
                "args": ""
            },
        }
        if action_type not in self.action_types.keys():
            raise NotImplementedError(
                f"Action type {action_type} not supported.\nChoose one of the following: {self.action_types.keys()}"
            )

    def produce_action(self):

        action_dict = self.action_types.get(self.action_type)
        popen_args = [action_dict.get("exe")]

        if action_dict.get("args"):
            popen_args.append(action_dict.get("args"))

        file_path = Path(self.path)
        if file_path.exists():
            popen_args.append(str(file_path))

        if self.args:
            popen_args.append(self.args)

        if self.action_type == "exe":
            popen_args = [file_path]


        logger.debug(f"Executing {' '.join(popen_args)}")
        print(f"Executing {' '.join(popen_args)}")

        return popen_args

