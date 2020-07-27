import npyscreen
from models import Task

class NewTaskForm(npyscreen.ActionFormV2):

    _DESCRIPTION_DEFAULT_TEXT = """Additional Context"""

    def __init__(self):

        super().__init__(name="Create New Task")

        self.title  = self.add(npyscreen.TitleText, name = "Task:",)
        self.due = self.add(npyscreen.TitleDateCombo, name = "Due:")
        self.description = self.add(npyscreen.MultiLineEdit,
               value = self._DESCRIPTION_DEFAULT_TEXT, name="Description: ",
               max_height=5, rely=5)
        self.priority = self.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One",
                values = ["low","medium","high","critical"], scroll_exit=True)
        self.tags = self.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], name="Tags",
                values = ["#help","#done","#needs"], scroll_exit=True)
    
    def on_ok(self):
        descr = self.description.value if self.description.value != self._DESCRIPTION_DEFAULT_TEXT else ""
        t = Task(
            self.title.value, 
            self.due.value, 
            descr, 
            self.readable_priority,
            self.readable_tags)
        t.save()
    
    @property
    def readable_priority(self):
        return self.priority.values[self.priority.value[0]]
    
    @property
    def readable_tags(self):
        return [self.tags.values[x] for x in self.tags.value]