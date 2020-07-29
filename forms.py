import npyscreen
from models import Task

class TaskList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(TaskList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "%s, %s" % (vl[1], vl[2])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').value =act_on_this[0]
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').value = None
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
        self.parent.update_list()

class TaskListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = TaskList
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.myDatabase.list_all_records()
        self.wMain.display()

class NewTaskForm(npyscreen.ActionFormV2):

    _DESCRIPTION_DEFAULT_TEXT = """Additional Context"""

    def __init__(self):

        super().__init__(name="Create New Task")

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
    
    def on_ok(self):
        descr = self.description.value if self.description.value != self._DESCRIPTION_DEFAULT_TEXT else ""
        t = Task(
            self.title.value, 
            self.due.value, 
            descr, 
            self.readable_priority,
            self.readable_status,
            self.readable_tags)
        t.save()
    
    @property
    def readable_priority(self):
        return self.priority.values[self.priority.value[0]]

    @property
    def readable_status(self):
        return self.status.values[self.status.value[0]]
    
    @property
    def readable_tags(self):
        return [self.tags.values[x] for x in self.tags.value]