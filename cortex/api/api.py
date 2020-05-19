import flask
import json
from ..saver import DatabaseDriver

app = Flask(__name__)
loader = None
@app.route('/users')
def get_users():
	'''Returns the list of all the supported users, including their IDs and names only.'''
	



def run_api_server(host, port, database_url):
	loader = DatabaseDriver(database_url)
	app.run(host=host,port=port)
	

