import npyscreen
from models import Task

class TaskList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(TaskList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, task):
        return f'{task.title} [{task.readable_priority}] ({task.readable_status[0]})'

    def actionHighlighted(self, selected_task, keypress):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').task = selected_task
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').value = None
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def when_delete_record(self, *args, **keywords):
        Task.delete(self.values[self.cursor_line])
        self.parent.update_list()

class TaskListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = TaskList
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = Task.get_all()
        self.wMain.display()

class TaskForm(npyscreen.ActionForm):

    _DESCRIPTION_DEFAULT_TEXT = """Additional Context"""

    def create(self):
        self.task = None
        self.title  = self.add(npyscreen.TitleText, name = "Task:",)
        self.due = self.add(npyscreen.TitleDateCombo, name = "Due:")
        self.description = self.add(npyscreen.MultiLineEdit,
               value = self._DESCRIPTION_DEFAULT_TEXT, name="Description: ",
               max_height=5, rely=5)
        self.priority = self.add(npyscreen.TitleSelectOne, max_height=4, value = [0,], name="Priority: ",
                values = Task._PRIORITIES, scroll_exit=True)
        self.status = self.add(npyscreen.TitleSelectOne, max_height=4, value = [0,], name="Status: ",
                values = Task._STATUS, scroll_exit=True)
        self.tags = self.add(npyscreen.TitleMultiSelect, max_height =-2, value = [], name="Tags: ",
                values = ["#help","#done","#needs"], scroll_exit=True)

    def beforeEditing(self):
        if self.task:
            self.title.value = self.task.title
            self.due.value = self.task.due
            self.description.value = self.task.description
            self.priority = [0,]
            self.status = [0,]
            self.tags.value = []
        else:
            self.title.value = ""
            self.due.value = None
            self.description.value = TaskForm._DESCRIPTION_DEFAULT_TEXT
            self.priority.value = [0,]
            self.status.value = [0,]
            self.tags.value = []
    
    def on_ok(self):
        descr = self.description.value if self.description.value != self._DESCRIPTION_DEFAULT_TEXT else ""
        if self.task and self.task.id:
            self.task.title = self.title.value, 
            self.task.due = self.due.value, 
            self.task.description = descr, 
            self.task.priority = self.priority.value[0],
            self.task.status = self.status.value[0]
            self.task.save()
        else:
            t = Task(
                title=self.title.value, 
                due=self.due.value, 
                description=descr, 
                priority=self.priority.value[0],
                status=self.status.value[0])
            t.save()
        self.parentApp.switchFormPrevious()
    
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    
    @property
    def readable_tags(self):
        return [self.tags.values[x] for x in self.tags.value]