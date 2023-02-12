import logging

from pathlib import Path
from time import sleep

import yaml

from punctual.scheduler import Scheduler
from punctual.tasks import Task


logger = logging.getLogger(__name__)


def main(task_file: str):
    scheduler = Scheduler()
    tasks = Path(task_file)

    while True:
        with tasks.open("r") as file:
            loaded_tasks = yaml.safe_load(file)

            for t in loaded_tasks.get('tasks'):
                try:
                    task = Task(
                        t.get('name'), t.get('state'),
                        t.get('first_run'), t.get('frequency'),
                        t.get('action'), t.get('toast')
                    )
                    scheduler.manage_tasks(task)
                except Exception as e:
                    print(e)
                    logger.error(f"Could not generate task from inputs: {e}")



        sleep(2)
