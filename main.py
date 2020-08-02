import signal
import sys

import npyscreen
from ui.mainForm import MainForm
from ui.taskEditForm import TaskEditForm
from ui.viewEditForm import ViewEditForm


# def ctrl_c_capture(sig, frame):
#     return

# signal.signal(signal.SIGINT, ctrl_c_capture)

class LollygagApplication(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="My Tasks")
        self.addForm("EDIT_TASK_FORM", TaskEditForm, name="Create Task")
        self.addForm("EDIT_VIEW_FORM", ViewEditForm, name="Create View")


if __name__ == "__main__":
    App = LollygagApplication()
    App.run()

