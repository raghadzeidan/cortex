import flask
from blessings import Terminal
from ..saver import DatabaseDriver
app = flask.Flask(__name__)
list_users = {"username":"Dan Gittk", "userId":"42"}, {"username":"Raghad Zeidan", "userId":"43"}
term = Terminal()
db = [{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"},
{"datetime":"2007","snapshotId":"422007", "feelings":{"hunger":0.5, "thirst":0.75, "exhaustion":1}, "pose":"stading", "color_image":"/home/user/Desktop/volume/color_images/images/42_1575446887339.png", "depth_image":"/home/user/Desktop/volume/depth_images/images/42_1575446887339.png"}]
quantity = 10
max_posts = 1000 #a reasonable maximum of snapshots to load

@app.route('/')
def main():
	return flask.render_template('test.html')
	
@app.route('/browse')
def  browse():
	return flask.render_template('browse.html', list_users=list_users)
	
	
@app.route("/users/<username>")
def profile(username):
	return flask.render_template('profile_template.html', username=username)
		
@app.route("/load/users/<username>")
def load(username):
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
	app.run(host, port)
