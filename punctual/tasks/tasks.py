from datetime import datetime

from punctual.tasks import Action


class Task(object):
    def __init__(self, name: str, state: str, first_run: dict, frequency: dict, action: dict, toast: dict = None):
        """
        Properties are derived from task file 'tasks' dictionary
        """

        freq_val = frequency.get('value')
        freq_fmt = frequency.get('format')

        default_dt = datetime.strptime('0', '%S')
        self.first_run = datetime.strptime(str(first_run.get("value")), first_run.get("format"))

        if freq_fmt in ["%d", "%m"] and freq_val == 1:
            freq_val = str(freq_val + 1)

        if freq_fmt in ["%y"] and len(str(freq_val)) < 4:
            freq_val = str(1900 + freq_val)

        dt_freq = datetime.strptime(str(freq_val), freq_fmt)

        dt_delta_freq = dt_freq - default_dt


        self.name = name
        self.state = state
        self.frequency = dt_delta_freq
        self.action = action
        self.toast = toast

        name = self.action.get('name')
        path = self.action.get('path')
        action_type = self.action.get('action_type')
        args = self.action.get('args')

        self.action_object = Action(name, path, action_type, args)


