import flask
import json
from ..saver import DatabaseDriver

app = flask.Flask(__name__)
loader = None

@app.route('/users')
def get_users():
	'''Returns the list of all the supported users, including their IDs and names only.'''
	users_list = loader.load_users()
	return json.dumps(users_list)
	
@app.route('/users/<int:uid>') #float not int?
def get_user(uid):
	user_info = loader.load_user_info(str(uid)) #ids are strs for some reason
	return json.dumps(user_info)
	
@app.route('/users/<int:uid>/snapshots')
def get_user_snapshots(uid):
	user_snapshots_list = loader.load_user_snapshots_list(str(uid))
	return json.dumps(user_snapshots_list)
	
@app.route('/users/<string:uid>/snapshots/<string:snapshotId>')
def get_snapshot(uid,snapshotId):
	print("YY" + str(snapshotId) + "YY" + str(uid))
	results_dic = loader.load_user_snapshot_results(uid, snapshotId)
	return json.dumps(results_dic)
	
@app.route('/users/<>')
def get_snapshot_result()
	
	


def run_api_server(host, port, database_url):
	global loader
	loader = DatabaseDriver(database_url)
	app.run(host=host,port=port)
	

