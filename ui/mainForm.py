import npyscreen
from ui.tasksBox import TasksBox
from ui.viewsBox import ViewsBox

class MainForm(npyscreen.FormBaseNew):

    def create(self):
        y, x = self.useable_space()

        self.viewsBoxComponent = self.add(
            ViewsBox, 
            name="Views", 
            value=0, 
            relx=1, 
            max_width=x // 5, 
            rely=2,
        )

        self.tasksBoxComponent = self.add(
            TasksBox, 
            name="Tasks",
            footer = "Current View: All Tasks",
            value=0,
            rely=2, 
            relx=(x // 5) + 1,
        )

        self.tasksBoxComponent.update_task_view()
        