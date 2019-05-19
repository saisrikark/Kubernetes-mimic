#sys.path.insert(0, '/path/to/application/app/folder')
import sys
sys.path.insert(0, 'dataaccess')
import categoriesFromDB
class categoriesListResponse:
	def __init__(self):
		self.categoryResponseDict = dict()

	def getCategoryResponseDict(self):
		return self.categoryResponseDict

	def fetchCategories(self):
		self.categoryResponseDict = categoriesFromDB.getCategoriesFromDB()

	def intializeDummy(self):
		self.categoryResponseDict['road_construction'] = 200
		self.categoryResponseDict['garbage_pickup'] = 150
		self.categoryResponseDict['kindness'] = 400
		self.categoryResponseDict['planting'] = 600


class category:
	def __init__(self,name):
		self.name = name

	def getCategoryName(self):
		return self.name