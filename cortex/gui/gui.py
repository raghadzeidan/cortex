import flask
from blessings import Terminal
from ..saver import DatabaseDriver
app = flask.Flask(__name__)
term = Terminal()
loader = None
quantity = 10
max_posts = 1000 #a reasonable maximum of snapshots to load

@app.route('/')
def main():
	return flask.render_template('test.html')
	
@app.route('/browse')
def  browse():
	list_users = loader.load_users() #empty input includes all fields as wanted.
	print(term.blue_on_white(str(list_users)))
	return flask.render_template('browse.html', list_users=list_users)
	
	
@app.route("/users/<uid>_<username>", methods=["GET","POST"])
def profile(uid,username):
	if flask.request.method=="POST":
		print("ZZZZZZZZZZZZZZZZZZZZZZZ",flask.request.form)
	return flask.render_template('profile_template.html', uid=uid, username=username)
		
@app.route("/load/users/<uid>_<username>")
def load(uid,username):
	'''This function returns a specified interval of the user's snapshots, which then are displayed on the screen
	dynamically '''
	db = loader.load_user_snapshots_list(str(uid), datetime=1, snapshotId=1, feelings=1, pose=1, color_image=1, depth_image=1)
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	res = None
	if flask.request.args:
		counter = int(flask.request.args.get("c"))
		if counter == 0:
			print(f"Returning posts 0 to {quantity}")
			res = flask.make_response(flask.jsonify(db[0: quantity]), 200)
			
		elif counter == max_posts:
			print("No more snapshots")
			res = flask.make_response(flask.jsonify({}), 200)
		else:
			print(f"Returning posts {counter} to {counter + quantity}")
			res = flask.make_response(flask.jsonify(db[counter: counter + quantity]), 200)
	print(res.get_data())
	return res
	

@app.route('/load/users/<uid>_<username>/<datetime>')
def get_snapshot_result(uid, snapshotId, result_name):
	results_dic = loader.load_user_result(uid,snapshotId, result_name)
	return_dic = {}
	if result_name == 'color-image' or result_name == 'depth-image':
		#we don't care about the actual path of the image (i.e results_dic), we're only publishing data url for get-purposes
		return_dic['data_url'] = f"/users/{uid}/snapshots/{snapshotId}/{result_name}/data"
	else:
		return_dic = results_dic #feelings and pose case
	return json.dumps(return_dic)
	
@app.route('/load/users/<uid>_<username>/<datetime>/<string:result_name>/data')
def get_image_data(uid, username, datetime, result_name):
	'''To get images as a get request from our server, which we then render on display. '''
	results_dic = loader.load_user_result(uid,f"{uid}_{datetime}", result_name)
	print(term.red_on_white(result_name + str(results_dic)))
	if result_name == "color-image": 
		path = results_dic['color_image']
	elif result_name == 'depth-image':
		path = results_dic['depth_image']
	else:
		return {}
	return flask.send_file(path, mimetype='image/gif')



@app.route('/users/<uid>_<username>/<datetime>')
def get_snapshot_of_user(uid, username, datetime):
	pose_results_dic = loader.load_user_result(uid,f"{uid}_{datetime}", "pose")['pose']
	feelings_results_dic = loader.load_user_result(uid,f"{uid}_{datetime}", "feelings")['feelings']
	modify_for_html(feelings_results_dic)
	print("ZZ"+ str(feelings_results_dic))
	return flask.render_template("snapshot_template.html", uid=uid, username=username, datetime=datetime, pose_dic = pose_results_dic, feelings_dic=feelings_results_dic)

def modify_for_html(feelings_dic):
	'''This function modifies the feelings dic for html purposes. '''
	print(term.red_on_white(str(feelings_dic)))
	for key in feelings_dic:
		print(term.blue_on_white(str(key)))
		print(term.blue_on_white(str(feelings_dic[key])))
		feelings_dic[key]=feelings_dic[key]*1000
	
def run_server(host, port, db_url):
	global loader
	loader = DatabaseDriver(db_url)
	app.run(host, port)
