import npyscreen
from forms import NewTaskForm

class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F  = NewTaskForm()

        # This lets the user interact with the Form.
        F.edit()

        #print(ms.get_selected_objects())
        #p = Project("my Project")
        #p.save()




if __name__ == "__main__":
    App = TestApp()
    App.run()

