import npyscreen
from npyscreen.wgmultiline import MultiLine
from models import Task
import curses

class TaskBoxMultiLine(MultiLine):

    def actionHighlighted(self, act_on_this, key_press):
        act_on_this += "XXXX"
        self.parent.parentApp.getForm('EDIT_TASK_FORM').value = None
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

class TasksBox(npyscreen.BoxTitle):

    _contained_widget = TaskBoxMultiLine

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').value = None
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def when_delete_record(self, *args, **keywords):
        Task.delete(self.tasks[self.cursor_line])
        self.update_task_view()

    def actionHighlighted(self, act_on_this, key_press):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').value = self.tasks[self.entry_widget.cursor_line]
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def update_task_view(self):
        
        self.tasks = Task.get_all()

        data = []
        color_data = []
        
        for task in self.tasks:
            row = f'{task.title} ({task.readable_priority}) [{task.readable_status}]'
            data.append(row)

        self.values = data 