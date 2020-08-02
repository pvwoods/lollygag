from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Boolean
from sqlalchemy.sql import text


Base = declarative_base()

class DB():
    engine = create_engine('sqlite:///dev.db')
    _SessionMaker = sessionmaker(bind=engine)
    __ACTIVE_SESSION = None

    def session():
        if not DB.__ACTIVE_SESSION:
            Base.metadata.create_all(DB.engine)
            DB.__ACTIVE_SESSION = DB._SessionMaker()
        return DB.__ACTIVE_SESSION

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
        s = DB.session()
        s.add(self)
        s.commit()
    
    def get_all():
        return DB.session().query(Task).all()

    def delete(task):
        s = DB.session()
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
        if not self.due:
            return "no due date"
        return self.due.strftime("%b %d %Y")

class View(Base):
    __tablename__ = 'views'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    query = Column(String)

    def get_tasks_for_view(self):
        return DB.session().query(Task).from_statement(text(self.query))
    
    def save(self):
        s = DB.session()
        s.add(self)
        s.commit()
    
    def get_all():
        return DB.session().query(View).all()

    def delete(view):
        s = DB.session()
        s.delete(view)
        s.commit()