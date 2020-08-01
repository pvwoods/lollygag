import uuid
import json
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Boolean


engine = create_engine('sqlite:///dev.db')
_SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()

def session_maker():
    Base.metadata.create_all(engine)
    return _SessionMaker()

class Task(Base):

    __tablename__ = 'tasks'

    _PRIORITIES = ["low", "medium", "high", "critical"]
    _STATUS = ["Open", "In Progress", "Blocked",  "Complete"]

    id = Column(Integer, primary_key=True)
    title = Column(String)
    due = Column(DateTime)
    description = Column(String)
    priority = Column(Integer)
    status = Column(Integer)

    def save(self):
        s = session_maker()
        s.add(self)
        s.commit()
    
    def get_all():
        return session_maker().query(Task).all()

    def delete(task):
        s = session_maker()
        s.delete(task)
        s.commit()

    @property
    def readable_priority(self):
        return Task._PRIORITIES[self.priority]

    @property
    def readable_status(self):
        return Task._STATUS[self.status]

    @property
    def readable_due(self):
        return self.due.strftime("%b %d %Y")



    # def __init__(self, title, due, description, priority, status, tags):
    #     self.title = title
    #     self.due = due
    #     self.description = description
    #     if priority in Task._PRIORITIES:
    #         self.priority = priority
    #     else:
    #         self.priority = Task._PRIORITIES[0]
    #     if status in Task._STATUS:
    #         self.status = status
    #     else:
    #         self.status = Task._STATUS[0]
    #     self.tags = tags

# class Collection(BaseObject):

#     def create_table_structure(db):
#         c = db.cursor()
#         c.execute(
#         f'CREATE TABLE IF NOT EXISTS ${type(self).__name__}\
#             ( _record_id INTEGER PRIMARY KEY, \
#               title     TEXT, \
#               due   TEXT, \
#               description   TEXT, \
#               priority   TEXT, \
#               description TEXT \
#               )' \
#             )
#         db.commit()
#         c.close()

#     def __init__(self, title):
#         self.title = title
#         self.tasks = [] # list of UUID references to tasks

# class Project(Collection):
#     def __init__(self, title):
#         super().__init__(title)

# class Tag(Collection):
#     def __init__(self, title):
#         super().__init__(title)