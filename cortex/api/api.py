import flask
import json
from blessings import Terminal
from ..saver import DatabaseDriver
term = Terminal()
app = flask.Flask(__name__)
loader = None

@app.route('/users')
def get_users():
	'''Returns the list of all the supported users, including their IDs and names only.'''
	users_list = loader.load_users(userId=1, username=1)
	return json.dumps(users_list)
	
@app.route('/users/<int:uid>') #float not int?
def get_user(uid):
	user_info = loader.load_user_info(str(uid)) #ids are strs for some reason
	return json.dumps(user_info)
	
@app.route('/users/<int:uid>/snapshots')
def get_user_snapshots(uid):
	'''Returns list of snapshots of user, with snapshotId and datetime only. '''
	user_snapshots_list = loader.load_user_snapshots_list(str(uid), datetime=1, snapshotId=1)
	return json.dumps(user_snapshots_list)
	
@app.route('/users/<string:uid>/snapshots/<string:snapshotId>')
def get_snapshot(uid,snapshotId):
	results_dic = loader.load_user_snapshot_results(uid, snapshotId)
	return json.dumps(results_dic)
	
@app.route('/users/<string:uid>/snapshots/<string:snapshotId>/<string:result_name>')
def get_snapshot_result(uid, snapshotId, result_name):
	results_dic = loader.load_user_result(uid,snapshotId, result_name)
	return_dic = {}
	if result_name == 'color-image' or result_name == 'depth-image':
		#we don't care about the actual path of the image (i.e results_dic), we're only publishing data url for get-purposes
		return_dic['data_url'] = f"/users/{uid}/snapshots/{snapshotId}/{result_name}/data"
	else:
		return_dic = results_dic #feelings and pose case
	return json.dumps(return_dic)
	
@app.route('/users/<string:uid>/snapshots/<string:snapshotId>/<string:result_name>/data')
def get_image_data(uid, snapshotId, result_name):
	results_dic = loader.load_user_result(uid,snapshotId, result_name)
	print(term.red_on_white(result_name + str(results_dic)))
	if result_name == "color-image": #name inconsistency
		path = results_dic['color_image']
	elif result_name == 'depth-image':
		path = results_dic['depth_image']
	else:
		return {}
	return flask.send_file(path, mimetype='image/gif')
	
def run_api_server(host, port, database_url):
	global loader
	loader = DatabaseDriver(database_url)
	app.run(host=host,port=port)
	

