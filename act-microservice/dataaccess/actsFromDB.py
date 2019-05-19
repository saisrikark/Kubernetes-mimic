from models import Acts
from app import db
import datetime

def convertTimeStampToReqFormat(timestamp):
	print("type of sqlalchemy datetime:",type(timestamp))
	date_string = datetime.datetime.strftime(timestamp,"%d-%m-%Y:%S-%M-%H")
	print("After COnversion:",date_string)
	return date_string

def getActsOfCategory(categoryName):
	'''
	returns a python list of acts belonging to a certain category
	'''
	actsOfCategory = Acts.query.filter_by(categoryName = categoryName).order_by(Acts.timestamp.desc()).all()
	print("Inside actsDB, acts of category query result:",actsOfCategory)
	resultList = []
	for act in actsOfCategory:
		details_dict = {}
		details_dict['actId'] = act.actId
		details_dict['username'] = act.username
		details_dict['timestamp'] = convertTimeStampToReqFormat(act.timestamp)
		details_dict['caption'] = act.caption
		details_dict['imageB64'] = act.imageB64
		details_dict['numvotes'] = act.numvotes
		details_dict['categoryName'] = act.categoryName
		resultList.append(details_dict)

	return resultList