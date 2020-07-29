import uuid
import json
import datetime
import sqlite3

class DB():

    def __init__(self, filename="lollygag.db", models=[]):
        self.dbfilename = filename
        db = sqlite3.connect(self.dbfilename)
        for model in models:
            model.create_table_structure(db)

class BaseObject():

    _record_id = None

    def create_table_structure(db):
        c = db.cursor()
        c.execute(
        f'CREATE TABLE IF NOT EXISTS ${type(self).__name__}\
            ( _record_id INTEGER PRIMARY KEY \
              )' \
            )
        db.commit()
        c.close()

    def save(self):
        if(self._uuid is None):
            self._uuid = uuid.uuid4()
        file_path = f'./scratchpad/{type(self).__name__}/{self._uuid.hex}.json'
        with open(file_path, 'w') as filehandle:
            filehandle.write(self.toJson())

class Task(BaseObject):

    _PRIORITIES = ["low", "medium", "high", "critical"]
    _STATUS = ["Open", "In Progress", "Blocked",  "Complete"]

    def create_table_structure(db):
        c = db.cursor()
        c.execute(
        f'CREATE TABLE IF NOT EXISTS ${type(self).__name__}\
            ( _record_id INTEGER PRIMARY KEY, \
              title     TEXT, \
              due   TEXT, \
              description   TEXT, \
              priority   TEXT, \
              description TEXT \
              )' \
            )
        db.commit()
        c.close()

    def __init__(self, title, due, description, priority, status, tags):
        self.title = title
        self.due = due
        self.description = description
        if priority in Task._PRIORITIES:
            self.priority = priority
        else:
            self.priority = Task._PRIORITIES[0]
        if status in Task._STATUS:
            self.status = status
        else:
            self.status = Task._STATUS[0]
        self.tags = tags

class Collection(BaseObject):

    def create_table_structure(db):
        c = db.cursor()
        c.execute(
        f'CREATE TABLE IF NOT EXISTS ${type(self).__name__}\
            ( _record_id INTEGER PRIMARY KEY, \
              title     TEXT, \
              due   TEXT, \
              description   TEXT, \
              priority   TEXT, \
              description TEXT \
              )' \
            )
        db.commit()
        c.close()

    def __init__(self, title):
        self.title = title
        self.tasks = [] # list of UUID references to tasks

class Project(Collection):
    def __init__(self, title):
        super().__init__(title)

class Tag(Collection):
    def __init__(self, title):
        super().__init__(title)