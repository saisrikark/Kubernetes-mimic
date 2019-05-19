
#selfielessacts/views/acts.py
from flask import Blueprint, request, jsonify, Response, abort
import requests
#from models import Acts
from models import Categories,Acts
from app import db
from validate.validateInput import validateAndFormatTimeFormat,validateImageFormat

acts = Blueprint('acts',__name__,url_prefix='/acts')

@acts.route('/upvote',methods=['POST'])
def upvote():
	if(request.method == 'POST'):
		json_data= request.get_json(force=True)
		if not json_data:
			print("Bad Request")
			return Response(status=400)
		else:
			#Assuming data is coming in an array
			act_id=json_data[0]
			req_act= Acts.query.filter_by(actId=act_id).first()
			if(not req_act):
				abort(400)
			#Assuming its a json object so just query and update
			#Should work will wait for the upload to be complete
			print(req_act.numvotes)
			req_act.numvotes+=1
			db.session.commit()
		return Response(status=200)


@acts.route('/<actID>',methods=['DELETE'])
def removeAct(actID):
    if (request.method == 'DELETE'):
        	pick_act= Acts.query.filter_by(actId=actID).first()
        	#text=pick_act.categoryName
        	if(not pick_act):
        		abort(400)
        	text = pick_act.categoryName
        	category = Categories.query.filter_by(categoryName=text).first()
        	category.numberOfActs -=1
        	db.session.delete(pick_act)
        	db.session.commit()
        	return Response(status=200)


@acts.route('',methods=['POST'])
def uploadAct():

	hostForGettingUsernames = "3.94.30.50"
	if (request.method == 'POST'):
	    json_data = request.get_json()
	    #print(json_data)
	    if (json_data):
	    	print("JSON is Valid")
	    	userNames = requests.get("http://{}:8080/api/v1/users".format(hostForGettingUsernames))
	    	try:
	    		userNames = userNames.json()
	    	except Exception as e:
	    		abort(400)

	    	if(len(userNames)>0):
	    		user_name = json_data['username']
	    		if(user_name):
	    			if(user_name in userNames):
	    				print("UserName is Present")
	    				act_id = json_data['actId']
				    	check_existing_id = Acts.query.filter_by(actId=act_id).first()
				    	print(check_existing_id)
				    	if not (check_existing_id):
				    		print("ID is Present")
				    		validationResult = validateAndFormatTimeFormat(json_data['timestamp'])
				    		if validationResult:
				    			print("Time is Valid")
				    			if validateImageFormat(json_data['imgB64']):
				    				print("Image is Valid")
				    				check_exisiting_category = Categories.query.filter_by(categoryName=json_data['categoryName']).first()
				    				#print(check_exisiting_category)
				    				if(check_exisiting_category):
				    					newAct=Acts(act_id,json_data['username'],
				    					validationResult,json_data['caption'],json_data['imgB64'],
				    					0,json_data['categoryName'])
				    					db.session.add(newAct)
				    					check_exisiting_category.numberOfActs+=1
				    					db.session.commit()
				    					return Response(status=200)
				    				else:
				    					return Response(status=400)					    				
				    			else:
				    				return Response(status=400)	
				    		else:
				    			return Response(status=400)
				    	else:
				    		abort(400)
	    			else:
	    				abort(400)
	    		else:
	    			abort(400)
	    	else:
	    		abort(400)
	    else:
	    	print("Bad Request")
	    	return Response(status=400)
	else:
		return Response(status=405)
