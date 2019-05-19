from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {"origins": 'http://localhost:5000'}})
'''
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'charset=utf-8'
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///selfieless.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = "cloud-cmoputing-pass"
db = SQLAlchemy(app)