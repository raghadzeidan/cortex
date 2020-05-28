import pika
import sys
import os
import json
import logging
import time
import random
import traceback
import datetime as dt
from ..mq import MQer
from blessings import Terminal
from google.protobuf.json_format import MessageToDict
import numpy as np
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from ..parsers import AVAILABLE_PARSERS
from .server_utils import TheUser, TheSnapshot
COUNTER = 0
logging.basicConfig()
term = Terminal()

USER_BISCUITS = {}
USERS_INFO = {} #Has mapping from user biscuit to his information
GENDER_MAP = {0:'m', 1:'f', 2:'o'}
server_mq = None

def get_available_parsers():
	return "@".join(AVAILABLE_PARSERS)
	
def biscuit_url(path):
	'''returns biscuit from URL, NONE if not legal URL '''
	parsed = path.split('/')
	if len(parsed) != 4:
		print('Bad client request')
		return None
	empty, user_id, user_biscuit, s = parsed
	if s != 'snapshot':
		print('Bad client request')
		return None
	if int(user_id) not in USER_BISCUITS:
		print('Client_id not registered')
		return None
	if USER_BISCUITS[int(user_id)] != user_biscuit:
		print('Bad request, biscuit does not match user ID')
		return None
	return user_biscuit

def check_bad_parser_error(parser_name):
	if parser_name not in AVAILABLE_PARSERS:
		print(term.red(f"Tried to send data of unsupported parser: {parser_name}"))
		raise TypeError
		
		
class JsonPrepareDriver():
	'''This class takes a snapshot and prepares its format from the client-server format
	(project-chosen protocol which is protobuf) and prepares it as a json format before 
	sending it through mq '''
	
	def __init__(self, biscuit, snapshot_data):
		'''using our unique biscuit, we extract user data.
		PROJECT: here we only use the client-server-protocol biscuit to extract the user
		data previously saved in the POST /hello of the user. couldn't find any way not to
		create a small relation between the protocol and the driver (the biscuit is the relation)'''
		self.snapshot = TheSnapshot()
		self.snapshot.ParseFromString(snapshot_data)
		self.biscuit = biscuit
		self.user = TheUser()
		user_data = USERS_INFO[biscuit]
		self.user.ParseFromString(user_data)
		self.volume_path = '/home/user/Desktop/volume'
	def stringify_datetime(self, datetime):
		return str(dt.datetime.fromtimestamp(datetime / 1e3))
		
	def prepare_to_publish(self):
		'''this is the main function of the driver. it takes the client-server protocol format 
		and prepares it to json format before sending to mq. '''
		global COUNTER
		to_publish = {}
		self.prepare_user_info(to_publish)
		date_string = self.stringify_datetime(self.snapshot.datetime)
		to_publish['datetime'] = date_string 
		self.prepare_feelings(to_publish)
		self.prepare_color_image(to_publish)
		self.prepare_pose(to_publish)
		self.prepare_depth_image(to_publish)
		
		print(term.green_on_black(f'Server Sending data {COUNTER} to Parsers...'))
		COUNTER = COUNTER + 1
		return json.dumps(to_publish)
		
	def prepare_user_info(self, to_publish):
		user_gender = GENDER_MAP[self.user.gender] #gets single character
		user_dict = MessageToDict(self.user)
		user_dict['gender'] = user_gender
		user_dict['birthday'] = self.stringify_datetime(user_dict['birthday'])
		to_publish['user']=user_dict
		
	def prepare_feelings(self, to_publish):
		check_bad_parser_error('feelings')
		feelings_dict = MessageToDict(self.snapshot.feelings)
		to_publish['feelings'] = feelings_dict
		
	def prepare_color_image(self, to_publish):
		'''saves color_image bytes in VOLUME/UDER_ID/DATETIME/color_image_data '''
		print(term.green_on_black(f'DEBUG RAGHD: datetime: {self.snapshot.datetime}'))
		datetime = self.snapshot.datetime
		path_suffix = f'/color_images/bytes/{self.user.user_id}_{datetime}'
		unique_img_path = self.volume_path + path_suffix
		with open(unique_img_path, 'wb') as f:
			print(term.green_on_white(f'type: {type(self.snapshot.color_image.data)}, length: {len(self.snapshot.color_image.data)}'))
			f.write(self.snapshot.color_image.data)
		color_img_dict = {}
		color_img_dict['width']=self.snapshot.color_image.width
		color_img_dict['height']=self.snapshot.color_image.height
		color_img_dict['data_path'] = unique_img_path
		to_publish['color_image'] = color_img_dict
		
	def prepare_pose(self, to_publish):
		translation_dict = MessageToDict(self.snapshot.pose.translation)
		rotation_dict = MessageToDict(self.snapshot.pose.rotation)
		pose_dict = {}
		pose_dict['translation'] = translation_dict
		pose_dict['rotation'] = rotation_dict
		to_publish['pose'] = pose_dict
	
	def prepare_depth_image(self, to_publish):
		'''saves color_image bytes in VOLUME/UDER_ID/DATETIME/depth_image_data '''
		datetime = self.snapshot.datetime
		path_suffix = f'/depth_images/bytes/{self.user.user_id}_{datetime}.npy'
		unique_depth_path = self.volume_path + path_suffix
		depth_dict = MessageToDict(self.snapshot.depth_image)
		float_array = depth_dict['data']
		np_array = np.reshape(float_array,(depth_dict['height'],depth_dict['width']))
		np.save(unique_depth_path,np_array, allow_pickle=False) #saving numpy 2D array
		
		depth_img_dict = {}
		depth_img_dict['width'] = self.snapshot.depth_image.width
		depth_img_dict['height'] = self.snapshot.depth_image.height
		depth_img_dict['data_path'] = unique_depth_path
		to_publish['depth_image'] = depth_img_dict
		
	@staticmethod
	def get_user_id(user_data):
		s_user = TheUser()
		s_user.ParseFromString(user_data)
		return s_user.user_id
		
		
		
DEFAULT_DRIVER = JsonPrepareDriver

	
class CortextServer(BaseHTTPRequestHandler):
	#prepare_driver = DEFAULT_PREPARE_DRIVER()
	def get_unique_biscuit(self, user_id):
		if user_id in USER_BISCUITS:
			return USER_BISCUITS[user_id]
		random8 = random.randint(10000000,99999999)
		user_biscuit = f'{user_id}{random8}' #guarantees uniqueness
		return user_biscuit
		
	def do_GET(self):
			try:
				self.send_response(200, get_available_parsers())
			except:
				logging.error("Error in initiating protocol")
				self.send_response(404)
			finally:
				self.end_headers()
			
	def do_POST(self):
		
			try:
				print(self.path)
				if self.path == '/hello':
					content_length = int(self.headers['Content-Length'])
					user_data = self.rfile.read(content_length)
					user_id = DEFAULT_DRIVER.get_user_id(user_data) #we need actual user ID.
					user_biscuit = self.get_unique_biscuit(user_id)
					USER_BISCUITS[user_id] = user_biscuit
					USERS_INFO[user_biscuit] = user_data 
					self.send_response(200, user_biscuit)
					
				elif (current_biscuit := biscuit_url(self.path)) is not None: 
					content_length = int(self.headers['Content-Length'])
					snapshot_data = self.rfile.read(content_length)
					self.send_response(200)
					driver = DEFAULT_DRIVER(current_biscuit, snapshot_data)
					test = driver.prepare_to_publish()
					#also needs decoupling (MQ)
					server_mq.create_exchange(exchange='parsers', exchange_type='fanout')
					server_mq.publish(exchange='parsers', key='', body=test)
					#channel.exchange_declare(exchange='parsers', exchange_type='fanout')
					#channel.basic_publish(exchange='parsers', routing_key='', body=test)
				else:
					print(term.red_on_white('Bad server URL'))
					raise TypeError(self.path)
			except Exception as e:
				logging.error("Error in receiving data in server")
				print(term.red(str(e)))
				traceback.print_exc(file=sys.stdout)
				self.send_response(404)
			finally:
				self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass


def run_server(host, port, mq_url):

	'''The protocol is an HTTP protocol between the server and his clinets.
	The protocol is as follows:
	Client first sends a /config GET request in order to received the available
	parsers in the framework(some client may not want to connect if available
	parsers is not suitable). if client chooses to connect, he then sends a /hello
	POST request, inside it there is the  user's datathe server then sends
	an OK response along with a biscuit, which is a unique number (user_id
	cont with a random 8-digit number) that then the clientcan POST
	/hello/biscuit/snapshot request in order to send snapshot (starts streaming
	snapshot in his own unique path). this is just for security measure,
	to prevent from 3rd parites to simply do a POST user_id/snapshot with
	a specific user_id biscuit are saved in a simple dictionary at server's
	end.'''
	global server_mq
	address = (host, int(port))
	server_mq = MQer(mq_url)
	httpd = ThreadedHTTPServer(address, CortextServer)
	logging.info('Starting Context Server.')
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		logging.info('Server Interrupted.')
		pass
	httpd.server_close()
	logging.info('Stopped Server.')


if __name__ == '__main__':
	print('hi')
