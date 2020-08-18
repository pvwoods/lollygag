import uuid
import json
import time

class LogAction():

    ACTION_TYPE_CREATE = 0
    ACTION_TYPE_UPDATE = 1

    def __init__(self, action_type, object_id, key, value):
        self.action_type = action_type
        self.key = key
        self.object_id = object_id
        self.value = value
        self.action_id = uuid.uuid4()
        self.creation_stamp = time.time()
    
    def serialize(self):
        return json.dumps({
            "action_id": self.action_id.hex,
            "object_id": self.object_id,
            "key": self.key,
            "value": self.value,
            "action_type": self.action_type,
            "creation_stamp": self.creation_stamp
        })

class MergableLog():

    def __init__(self):
        self._log = []
        self._action_id_lookup = set()
    
    def add(self, action):
        if action.action_id not in self._action_id_lookup:
            self._add(action)
            self.sort_log()
        else:
            raise Exception(f'action already exists: `{action.serialize()}`')
    
    def _add(self, action):
        self._log.append(action)
        self._action_id_lookup.add(action.action_id)

    def sort_log(self):
        self._log.sort(key = lambda x: (x.creation_stamp, x.action_id))
    
    def merge(self, other):
        for action in other._log:
            if action.action_id not in self._action_id_lookup:
                self._add(action)
        self.sort_log()


