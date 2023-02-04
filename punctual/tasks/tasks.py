from datetime import datetime

from punctual.tasks import Action


class Task(object):
    def __init__(self, name: str, state: str, first_run: dict, frequency: dict, action: dict, toast: dict = None):
        """
        Properties are derived from task file 'tasks' dictionary
        """

        default_dt = datetime.strptime('0', '%S')
        self.first_run = datetime.strptime(first_run.get('value'), first_run.get('format'))

        dt_freq = datetime.strptime(str(frequency.get('value')), frequency.get('format'))
        dt_delta_freq = dt_freq - default_dt

        self.name = name
        self.state = state
        self.frequency = dt_delta_freq
        self.action = action
        self.toast = toast

        name = self.action.get('name')
        path = self.action.get('path')

        self.action_object = Action(name, path)


