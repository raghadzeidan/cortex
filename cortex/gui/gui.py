import flask
from ..saver import DatabaseDriver
app = flask.Flask(__name__)


@app.route('/')
def main():
	return flask.render_template('test.html')


def run_server(host, port, db_url):
	app.run(host, port)
