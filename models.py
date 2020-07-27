import uuid
import json
import datetime

class BaseObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class BaseObject():

    _uuid = None

    def save(self):
        if(self._uuid is None):
            self._uuid = uuid.uuid4()
        file_path = f'./scratchpad/{self._uuid.hex}.json'
        with open(file_path, 'w') as filehandle:
            filehandle.write(self.toJson())
    
    def toJson(self):
        return json.dumps({**self.__dict__, **{ "_type": type(self).__name__ }}, cls=BaseObjectEncoder, sort_keys=True, indent=4)

class Task(BaseObject):

    _PRIORITIES = {"low": 1, "medium": 2, "high": 3, "critical": 4}

    def __init__(self, title, due, description, priority, tags):
        self.title = title
        self.due = due
        self.description = description
        if priority in self._PRIORITIES:
            self.priority = priority
        else:
            self.priority = "low"
        self.tags = tags

    @property
    def sort_score(self):
        return self.int_priority()

    def int_priority(self):
        return self._PRIORITIES[self.priority]

class Collection(BaseObject):

    def __init__(self, title):
        self.title = title
        self.tasks = [] # list of UUID references to tasks

class Project(Collection):
    def __init__(self, title):
        super().__init__(title)

class Tag(Collection):
    def __init__(self, title):
        super().__init__(title)