
import logging
import subprocess

import schedule

from punctual.tasks import Task

logger = logging.getLogger(__name__)


class Scheduler(object):
    def __init__(self):
        self.jobs = []
        self.running_tasks = []
        self.sched = schedule.Scheduler()

    def manage_tasks(self, task: Task):

        def executable_function():
            from windows_toasts import WindowsToaster, ToastText1
            if task.toast:
                try:
                    toaster = WindowsToaster(task.toast.get('title'))
                    toast_window = ToastText1()
                    toast_window.SetBody(task.toast.get('message'))
                    toaster.show_toast(toast_window)
                except Exception as e:
                    logger.error(f"Could not create toast message: {e}")

            try:
                subprocess.Popen(task.action_object.produce_action())
            except Exception as e:
                logger.error(f"Could not execute task: {e}")

        if task.name not in [i.name for i in self.running_tasks] and task.state != "absent":
            logger.error(f"Adding {task.name} to jobs")
            print(f"Adding {task.name} to jobs")
            secs = int(task.frequency.total_seconds())
            self.sched.every(secs).seconds.do(executable_function).tag(task.name)
            self.running_tasks.append(task)

        if task.name in [i.name for i in self.running_tasks] and task.state == "absent":
            logger.error(f"Removing {task.name} from jobs")
            job = self.sched.get_jobs(task.name)[0]
            print(f"Removing {task.name} from jobs")
            self.sched.cancel_job(job)

        self.sched.run_pending()




