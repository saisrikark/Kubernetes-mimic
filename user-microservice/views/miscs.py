from flask import Blueprint, render_template, request, jsonify, Response
from models import User
from app import db
from flask_cors import cross_origin

miscs = Blueprint('miscs',__name__,url_prefix='/miscs')

@miscs.route('/verify',methods=['POST'])
@cross_origin(headers=['Content-type','Accept'])
def verifyLogin():
	if request.method == 'POST':
		jsonData = request.get_json(force=True)
		username = jsonData['username']
		password = jsonData['password']
		existing = User.query.filter_by(username=username,password=password).first()
		print(existing)
		if(existing):
			string = '{"verify":"success"}'
			
		else:
			string = '{"verify":"failure"}'
		return Response(string,status=200)