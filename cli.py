
import os

from pathlib import Path

from punctual.config import config
from punctual.__main__ import main


punc_env = os.environ.get("PUNCPATH")
punc_path = Path(punc_env)

if not punc_env:
    appdata = os.environ.get("LOCALAPPDATA")
    punc_path = Path(appdata).joinpath("punc")

config_path = str(punc_path.joinpath("config.yml"))
tasks_path = str(punc_path.joinpath("tasks.yml"))


def run(config_file: str, task_file: str):
    config.configure_from_file(config_file)
    main(task_file)


if __name__ == "__main__":
    run(config_file=config_path, task_file=tasks_path)
