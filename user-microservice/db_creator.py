from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///selfieless.db', echo=True)
Base = declarative_base()
 
 
class User(Base):
    __tablename__ = "users"

    #id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, primary_key=True)
    password = Column(String)

    def __repr__(self):
        return "{}".format(self.username)
 
# create tables
Base.metadata.create_all(engine)