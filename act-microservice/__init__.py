#selfielessacts/__init__.py
from app import app
from db_setup import init_db
from flask_cors import CORS
from views.acts import acts
from views.categories import categories

base_url = '/api/v1'

#init_db()

app.register_blueprint(categories, url_prefix=base_url+'/categories')
app.register_blueprint(acts, url_prefix=base_url+'/acts')

@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.',500

if __name__=="__main__":
	#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
	app.run(host='0.0.0.0', port=80,debug=True)
	
