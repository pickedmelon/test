from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import TINYTEXT, TEXT, INTEGER, LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref

Base = declarative_base()


class Rawtext(Base):
    __tablename__ = 'rawtext'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(INTEGER, primary_key=True)
    uri = Column(String(128), nullable=False, unique=True)
    html = Column(LONGTEXT, nullable=False)


class Snippet(Base):
    __tablename__ = 'snippet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(INTEGER, primary_key=True)
    rawtext_id = Column(INTEGER, ForeignKey("rawtext.id"), nullable=False)
    snippet_text = Column(TEXT, nullable=False)
    rawtext = relationship("Rawtext", backref=backref('snippets', lazy='noload'))


class Reference(Base):
    __tablename__ = 'reference'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(INTEGER, primary_key=True)
    snippet_id = Column(INTEGER, ForeignKey("snippet.id"), nullable=False)
    reference_text = Column(TEXT, nullable=False)
    snippet = relationship("Snippet", backref=backref('references', lazy='noload'))



engine = create_engine('mysql://law:watermelon@localhost/smartlaw?charset=utf8')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)


def execute_with_session(cmd):
    return get_with_session(lambda s: s.execute(cmd))


def add_with_session(newobj):
    try:
        session = scoped_session(session_factory)
        if type(newobj) is list:
            if len(newobj) > 0:
                session.add_all(newobj)
        else:
            session.add(newobj)
        session.commit()
        return newobj
    except:
        print "Exeception adding objs"
        pass
    finally:
        session.remove()


def get_with_session(query):
    try:
        session = scoped_session(session_factory)
        return query(session)
    except:
        pass
    finally:
        session.remove()
