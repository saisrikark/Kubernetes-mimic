from app import db

class Categories(db.Model):
 	__tablename__ = "categories" 
 	#id = db.Column(db.Integer,primary_key=True)
 	categoryName = db.Column(db.String, primary_key=True)
 	numberOfActs = db.Column(db.Integer)
 	acts = db.relationship('Acts', backref='categories', lazy=True)

 	def __init__(self,categoryName,numberOfActs):
 		self.categoryName = categoryName
 		self.numberOfActs = numberOfActs
 	def __repr__(self):
 		return "<CategoryName: {} - {}>".format(self.categoryName,self.numberOfActs)

class Acts(db.Model):
	__tablename__ = "acts"
	actId = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String,nullable=False)
	timestamp = db.Column(db.DateTime)
	caption = db.Column(db.String)
	imageB64 = db.Column(db.String,nullable=False)
	numvotes = db.Column(db.Integer)
	categoryName = db.Column(db.String, db.ForeignKey('categories.categoryName'),
		nullable=False)

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