import sys
sys.path.insert(0, 'datatypes')
import categoriesList
#from categoriesList import category
from models import Categories
from app import db

def getCategoriesFromDB():
	categoriesOfDB = dict()
	categoriesList = db.session.query(Categories).all()
	for eachCategory in categoriesList:
		#print(eachCategory)
		print(eachCategory.categoryName,eachCategory.numberOfActs)
		categoriesOfDB[eachCategory.categoryName] = eachCategory.numberOfActs
	return categoriesOfDB


def addCategoryDB(category):
	print("Inside add category, the category object received:",category)
	print("Name of the category object:",category.getCategoryName())
	existing = Categories.query.filter_by(categoryName = category.getCategoryName()).first()
	print("Any existing category of same name:",existing)
	if(existing):
		return False
	newCategory = Categories(category.getCategoryName(),0)
	db.session.add(newCategory)
	db.session.commit()
	return True

def deleteCategoryDB(categoryName):
	print(categoryName)
	retrieve_category = Categories.query.filter_by(categoryName = categoryName).first()
	if(retrieve_category):
		Categories.query.filter_by(categoryName = categoryName).delete()
		db.session.commit()
		return True
	else:
		return False

def getCategoryDetails(categoryName):
	'''
	returns the details of category with categoryName.
	'''
	print("Getting details for category",categoryName)
	retrieved_category = Categories.query.filter_by(categoryName = categoryName).first()
	if not retrieved_category:
		print("Couldn't retrieve category details")
		return {}
	else:
		details_dict = dict()
		details_dict['categoryName'] = retrieved_category.categoryName
		details_dict['numberOfActs'] = retrieved_category.numberOfActs
		return details_dict