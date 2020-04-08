import pika
import sys
import os
import json
import logging
import time
import random
import flask
from blessings import Terminal
from google.protobuf.json_format import MessageToDict
#import utils.render as render
#from utils import Connection, Listener
#from thought import Thought, render_from_bytes
import concurrent.futures as cf
#import pika
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from ..parsers import AVAILABLE_PARSERS
from .server_utils import TheUser, TheSnapshot
#from .server_utils import JsonPrepareDriver
THREADS_NUMBER = 5
METADATA_LENGTH = 20
COUNTER = 0
logging.basicConfig()
term = Terminal()
USER_BISCUITS = {}
USERS_INFO = {} #Has mapping from user biscuit to his information
GENDER_MAP = {0:'m', 1:'f', 2:'o'}
params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def get_available_parsers():
	return "@".join(AVAILABLE_PARSERS)
	
def biscuit_url(path):
	'''returns biscuit from URL, NONE if not legal URL '''
	parsed = path.split('/')
	#print("PARSED",parsed,"LENG",len(parsed))
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

class JsonPrepareDriver():
	'''This class takes a snapshot and prepares its format from the client-server format
	(project-chosen protocol which is protobuf) and prepares it as a json format before 
	sending it through mq '''
	def prepare_to_publish(self, biscuit, snapshot):
		global COUNTER
		to_publish = {}
		
		user = USERS_INFO[biscuit]
		volume_path = '/home/user/Desktop/volume'
		
		user_gender = GENDER_MAP[user.gender] #gets single character
		user_dict = MessageToDict(user)
		user_dict['gender'] = user_gender
		to_publish['user_info']=user_dict
		
		
		feelings_dict = MessageToDict(snapshot.feelings)
		to_publish['feelings']=feelings_dict
		
		unique_img_path = f'{volume_path}/{biscuit}'
		with open(unique_img_path, 'wb') as f:
			f.write(snapshot.color_image.data)
		color_img_dict = {}
		color_img_dict['width']=snapshot.color_image.width
		color_img_dict['height']=snapshot.color_image.height
		color_img_dict['data_path'] = unique_img_path
		to_publish['color_image'] = color_img_dict
		#print(term.green_on_black(f'Server Sending data {COUNTER} to Parsers...'))
		COUNTER = COUNTER + 1
		#return json.dumps(to_publish)
		return 'YES'

default_prepare_driver = JsonPrepareDriver()

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
					received_data = self.rfile.read(content_length)
					user = TheUser()
					user.ParseFromString(received_data)
					#print(type(user.gender))
					#print(term.red_on_white(str(user) + "TYPE:" + type(user) + "GENDER" + str(user.gender)))
					user_biscuit = self.get_unique_biscuit(user.user_id)
					USER_BISCUITS[user.user_id] = user_biscuit
					USERS_INFO[user_biscuit] = user #saves user informationwith relevant biscuit
					self.send_response(200, user_biscuit)
				elif (current_biscuit := biscuit_url(self.path)) is not None:
					content_length = int(self.headers['Content-Length'])
					received_data = self.rfile.read(content_length)
					self.send_response(200)
					#snapshot = TheSnapshot()
					#snapshot.ParseFromString(received_data)
					#test = default_prepare_driver.prepare_to_publish(current_biscuit, snapshot)					
					print(term.green_on_black('Server sleeping for 5 seconds before printing data'))
					time.sleep(5)
					print(received_data)
					#channel.exchange_declare(exchange='parsers', exchange_type='fanout')
					#channel.basic_publish(exchange='parsers', routing_key='', body=test)
				else:
					print(term.red_on_white('Bad server URL'))
					raise TypeError('self.path')
			except Exception as e:
				logging.error("Error in receiving data in server")
				print(term.red(str(e)))
				self.send_response(404)
			finally:
				self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass
    
#TODO:bad practice, consider puting them as default args (Server and the serverClass)
def run_server(host, port):
	'''The protocol is an HTTP protocol between the server and his clinets.
	The protocol is as follows:
		Client first sends a /config GET request in order to received the available parsers in the framework
		(some client may not want to connect if available parsers is not suitable).
		if client chooses to connect, he then sends a /hello POST request, inside it there is the user's data
		the server then sends an OK response along with a biscuit, which is a unique number (user_id cont with a random 8-digit number) that then the client
		can POST /hello/biscuit/snapshot request in order to send snapshot (starts streaming snapshot in his own unique path)
		this is just for security measure,  to prevent from 3rd parites to simply do a POST user_id/snapshot with a specific user_id
		biscuit are saved in a simple dictionary at server's end.''' 
	address = (host, int(port))
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

