import flask
from blessings import Terminal
from ..saver import DatabaseDriver
app = flask.Flask(__name__)
term = Terminal()
loader = None
quantity = 5
max_posts = 1000 #a reasonable maximum of snapshots to load

@app.route('/')
def main():
	return flask.render_template('test.html')
	
@app.route('/browse')
def  browse():
	list_users = loader.load_users() #empty input includes all fields as wanted.
	print(term.blue_on_white(str(list_users)))
	return flask.render_template('browse.html', list_users=list_users)
	
	
@app.route("/users/<uid>_<username>")
def profile(uid,username):
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

def run_server(host, port, db_url):
	global loader
	loader = DatabaseDriver(db_url)
	app.run(host, port)
