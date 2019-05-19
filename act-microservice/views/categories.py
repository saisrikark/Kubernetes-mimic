#selfielessacts/views/acts.py
from flask import Blueprint, render_template, request, jsonify, Response
from flask_cors import cross_origin
import sys
import json
sys.path.insert(0, 'datatypes')
sys.path.insert(1,'dataaccess')
import categoriesList
import categoriesFromDB
import actsFromDB

categories = Blueprint('categories',__name__)

@categories.route('',methods=['GET','POST'])
@cross_origin(headers=['Content-type','Accept'])
def addOrList():
	#If GET, list
	#If POST, add

	# Get List of Categories
	if (request.method == 'GET'):
		categoriesListResponse = categoriesList.categoriesListResponse()
		#categoriesListResponse.intializeDummy()
		categoriesListResponse.fetchCategories()
		response = jsonify(categoriesListResponse.getCategoryResponseDict())
		print(response)
		return response

	# Add Category
	if (request.method == 'POST'):
		json_data = request.get_json(force=True)
		if not json_data:
			print("Bad Request")
			return Response(status=400)
		else:
			json_data_dump = json.loads(json.dumps(json_data))
			print("The json_data_dump:",json_data_dump)
			categoryName = categoriesList.category(json_data_dump[0])
			print("Made a new category object:",categoryName.getCategoryName())
			result = categoriesFromDB.addCategoryDB(categoryName)
			if(result):
				return Response(status=201)
			else:
				return Response(status=400)
	'''
	if(request.method == 'DELETE'):
		pass
	else:
		return Response(status=405)
	'''
                

@categories.route('/<categoryName>',methods=['DELETE'])
@cross_origin(headers=['Content-type','Accept'])
def deleteCategory(categoryName):
	#IF DELETE, remove the category
	if(request.method == 'GET'):
		return Response(status=405)
	if(request.method == 'DELETE'):
		#print(categoryName)
		if(categoryName == ""):
			return Response(status=400)
		result = categoriesFromDB.deleteCategoryDB(categoryName)
		if(result):
			return Response(status=200)
		else:
			return Response(status=400)

@categories.route('/<categoryName>/acts',methods=['GET'])
@cross_origin(headers=['Content-type','Accept'])
def listActs(categoryName):
	#If num acts<100, return all the acts in this category
	#else, error
	if(request.method == 'GET'):
		#first check if category exists
		categoryDetails = categoriesFromDB.getCategoryDetails(categoryName)
		if not categoryDetails:
			#if category doesn't exist
			#return status 204 [No Response Body]
			return Response(status=204)

		#Check if range was specified
		start = request.args.get('start')
		end = request.args.get('end')

		if not start and not end:
			print('no headrs')
			#category was found, check the number of acts
			if categoryDetails['numberOfActs']>100:
				#number of acts is too many
				#so send status 413
				return Response(status=413)

			result = jsonify(actsFromDB.getActsOfCategory(categoryName))
			print("jsonified result of listActs:",result)
			return result

		else:
			end = int(end)
			start = int(start)
			#Number of acts is greater than 100 so say that too difference
			if(end-start>100):
				return Response(status=413)

			#category was found, check the number of acts
			if categoryDetails['numberOfActs']==0:
				#Empty category
				return Response(status=204)

			acts_list=actsFromDB.getActsOfCategory(categoryName)
			if(len(acts_list)<start or len(acts_list)<end):
				return Response(status=204)
			else:
				return jsonify(acts_list[start-1:end])
			

	else:
		return Response(status=405)

@categories.route('/<categoryName>/acts/size',methods=['GET'])
@cross_origin(headers=['Content-type','Accept'])
def getActSize(categoryName):
	'''
	return number of acts in the category
	'''
	if(request.method == 'GET'):
		detailsOfCategory = categoriesFromDB.getCategoryDetails(categoryName)
		print("category details dict:",detailsOfCategory)

		#check if category even exists
		if not detailsOfCategory:
			return Response(status=204)
		else:
			result = jsonify([detailsOfCategory['numberOfActs']])
			return result
