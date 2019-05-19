#selfielessacts/views/acts.py

from flask import Blueprint, request, jsonify, Response, abort
from models import User
from app import db
from dataaccess.users import listUsers
from flask_cors import cross_origin
from validate.validateInput import validatePassword

users = Blueprint('users',__name__)

@users.route('', methods=['POST','GET'])
@cross_origin(headers=['Content-type','Accept'])
def addUser():
	#only POST
	#add user
	if(request.method == 'GET'):
		listOfUsers = listUsers()
		if(len(listOfUsers) == 0):
			return Response('{}',status=204)
		else:
			print(listOfUsers)
			return jsonify(listOfUsers)
	if(request.method == 'POST'):
		jsonData = request.get_json(force=True)
		username = jsonData['username']
		password = jsonData['password']
		if(validatePassword(password)):
			print(username, password)

			existing = User.query.filter_by(username=username).first()
			if(existing):
				abort(400)

			newUser = User(username, password)
			db.session.add(newUser)
			db.session.commit()

			return Response('{}',status=201)
		else:
			return Response(status=400)
	else:
		return Response(status=405)


@users.route('/<userName>', methods=['DELETE'])
@cross_origin()
def deleteUser(userName):
	#DELETE
	#remove the user
	if(request.method == 'DELETE'):
		retrieved_user  = User.query.filter_by(username=userName).first()
		if(retrieved_user):
			User.query.filter_by(username=userName).delete()
			db.session.commit()
			return Response(status=200)
		else:
			return Response(status=400)
	else:
		return Response(status=405)
