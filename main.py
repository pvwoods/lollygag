import npyscreen
from forms import TaskForm, TaskListDisplay

class LollygagApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("MAIN", TaskListDisplay)
        self.addForm("EDIT_TASK_FORM", TaskForm)


if __name__ == "__main__":
    App = LollygagApplication()
    App.run()

