import flask
import json
from ..saver import DatabaseDriver

app = flask.Flask(__name__)
loader = None

@app.route('/users')
def get_users():
	'''Returns the list of all the supported users, including their IDs and names only.'''
	return loader.load_users()
	


def run_api_server(host, port, database_url):
	global loader
	loader = DatabaseDriver(database_url)
	app.run(host=host,port=port)
	

