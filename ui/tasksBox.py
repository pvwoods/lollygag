import npyscreen
from npyscreen.wgmultiline import MultiLineAction
from models import Task
import curses

class TaskBoxMultiLine(MultiLineAction):

    def __init__(self, *args, **keywords):
        super(TaskBoxMultiLine, self).__init__(*args, **keywords)
        self.add_handlers({
            "^D": self.when_delete_record
        })
        self.update_tasks()
    
    def display_value(self, task):
        return f'{task.title} ({task.readable_priority}) [{task.readable_status}]'

    def actionHighlighted(self, selected_task, key_press):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').task = selected_task
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def when_delete_record(self, *args, **keywords):
        Task.delete(self.values[self.cursor_line])
        self.update_tasks()

    def update_tasks(self):
        self.values = Task.get_all()

class TasksBox(npyscreen.BoxTitle):

    _contained_widget = TaskBoxMultiLine

    def __init__(self, *args, **keywords):
        super(TasksBox, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record
        })

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').task = None
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')
    
    def update_view(self):
        self.entry_widget.update_tasks()