import signal
import sys
from lollygag.app import LollygagApplication


def ctrl_c_capture(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c_capture)

if __name__ == "__main__":
    App = LollygagApplication()
    App.run()

