import signal
import sys

import npyscreen
from forms import TaskForm, TaskListDisplay


def ctrl_c_capture(sig, frame):
    return

signal.signal(signal.SIGINT, ctrl_c_capture)

class LollygagApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("MAIN", TaskListDisplay)
        self.addForm("EDIT_TASK_FORM", TaskForm)


if __name__ == "__main__":
    App = LollygagApplication()
    App.run()

