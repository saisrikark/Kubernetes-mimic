from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///selfieless.db', echo=True)
Base = declarative_base()
 
class Categories(Base):
 	__tablename__ = "categories" 
 	#id = Column(Integer,primary_key=True, autoincrement=True)
 	categoryName = Column(String, primary_key=True)
 	numberOfActs = Column(Integer)
 	acts = relationship('Acts', backref='categories', lazy=True)

class Acts(Base):
	__tablename__ = "acts"
	actId = Column(Integer,primary_key=True)
	username = Column(String,nullable=False)
	timestamp = Column(DateTime)
	caption = Column(String)
	imageB64 = Column(String,nullable=False)
	numvotes = Column(Integer)
	categoryName = Column(Integer,ForeignKey('categories.categoryName'))
	def __init__(self,actId,username,timestamp,caption,imageB64,numvotes,categoryName):
		self.actId = actId
		self.username = username
		self.timestamp = timestamp
		self.caption = caption
		self.imageB64 = imageB64
		self.numvotes = numvotes
		self.categoryName = categoryName

	def __repr__(self):
 		return "<Acts: {} - {} - {} - {}>".format(self.actId,self.username,self.numvotes,self.categoryName) 	
# create tables
Base.metadata.create_all(engine)