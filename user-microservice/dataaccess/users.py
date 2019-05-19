from models import User
from app import db

def listUsers():
	return [i.username for i in User.query.all()]
