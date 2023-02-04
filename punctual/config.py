import json
import logging
import logging.config
import os
import sys
from pathlib import Path

import yaml

if os.name == 'nt':
    win_ver = sys.getwindowsversion()
    if win_ver.major == 10:
        os_config = "Windows"
    else:
        raise OSError(f"Windows {win_ver.major} is not supported")
else:
    os_config = "Posix"


class Config:
    def __init__(self):
        self.configured = False
        self.base_dir = Path(__file__).resolve().parent
        self.config_file_path = ""
        self.config_file = ""

        self.threads = os.cpu_count()-1
        self.task_file = ""
        self.logs_dir = ""
        self.log_config = None

    def configure_from_file(self, config_file_path):
        self.config_file_path = config_file_path

        if Path(self.config_file_path).exists():
            self.config_file = self.config_file_path

        loaded_config = {}
        if self.config_file:
            if self.config_file.endswith((".yaml", ".yml")):
                with open(self.config_file, "r") as file:
                    loaded_config = yaml.safe_load(file)
            elif self.config_file.endswith(".json"):
                with open(self.config_file, "r") as file:
                    loaded_config = json.load(file)
            for attr in loaded_config.keys():
                if hasattr(self, attr):
                    attr_value = loaded_config[attr]
                    if isinstance(loaded_config[attr], str) and loaded_config[attr][0] == '~':
                        attr_value = loaded_config[attr].replace("~", str(Path.home()))
                    setattr(self, attr, attr_value)

        self.configured = True
        self.configure_logging()

    # noinspection PyBroadException
    def configure_logging(self):
        if self.configured and self.log_config:
            log_filename = None
            try:
                log_filename = self.log_config.get("handlers").get("file").get("filename")
            except:
                pass

            if log_filename and Path(self.logs_dir).exists():
                Path(self.logs_dir).joinpath(log_filename).touch()
                if (self.log_config.get("handlers")
                        and self.log_config["handlers"].get("file")
                        and self.log_config["handlers"]["file"].get("filename")):
                    self.log_config["handlers"]["file"]["filename"] = Path(self.logs_dir).joinpath(log_filename)

            logging.config.dictConfig(self.log_config)


config = Config()
