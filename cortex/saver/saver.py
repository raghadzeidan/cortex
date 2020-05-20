import pymongo
from furl import furl
import json
import logging
from blessings import Terminal
from ..mq import MQer
term = Terminal()
def find_db_driver(furl_object):
	db = furl_object.scheme
	if db in DB_DRIVERS:
		return db
	logging.error('invalid DB URL - Saver')
	raise TypeError(f'Unsupported database {db}')
	
class MongoDriver():
	
	def __init__(self, host, port):
		print(host, port)
		self.client = pymongo.MongoClient(host=host, port=port)
		self.db = self.client.db
		self.users = self.db.users
		
		
	def first_one(self, current_snapshot_id):
		'''this function is applied after every data recieved from
		saver that need to be saved, he first cheks if some other data 
		has already arrive that belongs in the same snapshot, by checking
		if someone else has already put the unique snapshot id which is
		user_id#datetime of that snapshot '''
		#this implies someone has submitted something to this user_id#datetime combo already
		result = self.users.find_one({'_id':current_snapshot_id}) 
		print(result)
		return False if result else True #result should be null if nothing is found.
		
	def validate_user_document(self, user_info_dict):
		'''This function inserts the user ID and user information (metadata) if necessary.
		If a user's document does not already exist from previously entered snapshots,
		this functions creates it utilizing the upsert flag in update_one function.
		if the users document already exists (i.e, a document with _id={the users's ID} along with
		"user_info": {dictionary of User's metadata}), the function doesn't do anything.'''
		user_id = user_info_dict['userId']
		self.users.update_one({"_id":user_id}, {"$set":{"_id":user_id}}, upsert=True)
		self.users.update_one({"_id":user_id}, {"$set": {"user_info":user_info_dict}}, upsert=True)
		
	def validate_snapshot_document(self, user_id, datetime):
		'''This function makes sure that the current snapshot document is allocated inside
		the array of the snapshot of the relevant user. the "allocation" should be applied whenever
		the "length" of the document retreieved from the server are of length 1. If it is of length 2
		that means that someone has already allocated a dictionariy depiciting the current snapshot with "datetime" 
		already in it. that is the protocol. '''
		result = self.users.find_one({"_id":user_id}, {"snapshots":{"$elemMatch":{"datetime":datetime}}})
		result_length = len(result)
		print(f"result length = {result_length}")
		if result_length == 1: #if first one here, then should initialize the datetime inside current snapshot document in the users' snapshots array
			self.users.update_one({"_id":user_id}, {"$push":{"snapshots":{"datetime":datetime}}})#push generates array automatically
		elif result_length !=2:
			raise TypeError('something went wrong in the database.')
		
	def save(self, data_name ,data):
		'''this function receives a data_name to be save and dictionary of
		that data, after being converted into the relevant-expected format (dictionary) '''
		
		user_id = data['user']['userId']
		datetime = data['datetime']
		
		self.validate_user_document(data['user']) #creating user's db document if necessary.
		self.validate_snapshot_document(user_id, datetime)
		
		data_dic = data[data_name] #PROJECT: example: data_name = "color_image", data[dataname] = "dekstop/volume/color_img.png"
		
		self.users.update_one({"_id":user_id,"snapshots.datetime":datetime},{"$set":{ f"snapshots.$.{data_name}":data_dic}})
		print(term.red_on_white("X"))
		print(data_name + str(data_dic))
		print(term.red_on_white("X"))
		
	def load_users(self):
		return self.users.find({},{"user_info":1, "_id":0})
		
		


class JsonToMongo():
	'''this driver converts from the MQ format to the DB Driver format
	in our case, the MQ protocol is json and the driver is mongo
	the driver expected python dictionaries, so simple json.loads sufficies.
	for more complicated formats other than json that might have been used, this
	class could be benefitial '''
	def convert(self, data):
		return json.loads(data)

class MongoToJson():
	'''This driver converts from DB format to the format that the API works in.
	in our cause, this converting-driver expects cursor of MONGODB type, and processes them
	according to the rest-api desires and returns in JSON format. '''
	def convert_users_list(self, cursor):
		array = list(cursor)
		return json.dumps(array)
		
DB_DRIVERS = {'mongodb':  MongoDriver}
DB_SUPPORTED_FORMATS = {'feelings', 'color_image', 'depth_image', 'pose'}
MQ_TO_DB_DRIVER = JsonToMongo
DB_TO_API_DRIVER = MongoToJson

class DatabaseDriver:
	
	def __init__(self, url):
		furl_object = furl(url)
		port = furl_object.port
		host = furl_object.host
		driver_name = find_db_driver(furl_object)
		DBDriver = DB_DRIVERS[driver_name]
		self.db_driver = DBDriver(host, port)
		self.data_convert_driver = MQ_TO_DB_DRIVER()
		self.db_to_api_driver = DB_TO_API_DRIVER()
		
	def find(self, data_format, data):
		return True
		
	def save(self, data_format, data):
		if data_format not in DB_SUPPORTED_FORMATS:
			logging.info(f'Unsupported data-format to save: {data_format}')
			raise TypeError(f'Unsupported data-format to save: {data_format}')
		data_converted = self.data_convert_driver.convert(data) #dioctionary-ed and ready to go.
		self.db_driver.save(data_format, data_converted)
	def load_users(self):
		data_retreived = self.db_driver.load_users()
		users_list_json = self.db_to_api_driver.convert_users_list(data_retreived)
		return users_list_json
		
	
		
