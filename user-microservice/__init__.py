#selfielessacts/__init__.py
from app import app
from db_setup import init_db
from flask_cors import CORS
from views.users import users
from views.miscs import miscs

base_url = '/api/v1'

#init_db()

app.register_blueprint(users, url_prefix=base_url+'/users')
app.register_blueprint(miscs, url_prefix=base_url+'/miscs')

@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.',500

if __name__=="__main__":
	#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
	app.run(host='0.0.0.0', port=80,debug=True)
	
