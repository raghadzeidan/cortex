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
		return False if result else True
		
	def save(self, data_name ,data):
		'''this function receives a data_name to be save and dictionary of
		that data, after being converted into the relevant-expected format (dictionary) '''
		#print(term.red_on_white(str(data)))
		user_id = data['user']['userId']
		datetime = data['datetime']
		
		#unique snapshot ID indicating the place in DB which snapshot is saved. 
		#this is to gather multiple data from parsers that belong to same snapshot together.
		current_snapshot_id = f'{user_id}#{datetime}' 
		x = self.users.find()
		#for z in x:
		#	print(term.blue_on_white(str(z)))
		if self.first_one(current_snapshot_id):
			print('hi')
			self.users.insert_one({'_id':current_snapshot_id}) #unique _id of current snapshot is user_id#datetime
			print(term.yellow_on_white(f'{data_name} is here first, metada has been set'))
		
		data_dic = data[data_name]
		search_dic = {'_id':current_snapshot_id}
		result = self.users.update_one(search_dic, {'$set': {data_name:data_dic}})
		print(term.red_on_white(f'Data of {data_name} saved'))
		if not result:
			raise ValueError(f"Something went wrong with saving data: user ID: {user_id}, datetime: {datetime}, data name: {data_name}")
		
		
		


class JsonOUTtoMongoIN():
	'''this driver converts from the MQ format to the DB Driver format
	in our case, the MQ protocol is json and the driver is mongo
	the driver expected python dictionaries, so simple json.loads sufficies.
	for more complicated formats other than json that might have been used, this
	class could be benefitial '''
	def convert(self, data):
		return json.loads(data)

DB_DRIVERS = {'mongodb':  MongoDriver}
DB_SUPPORTED_FORMATS = {'feelings', 'color_image', 'depth_image', 'pose'}
MQ_TO_DB_DRIVER = JsonOUTtoMongoIN

class Saver:
	
	def __init__(self, url):
		furl_object = furl(url)
		port = furl_object.port
		host = furl_object.host
		driver_name = find_db_driver(furl_object)
		DBDriver = DB_DRIVERS[driver_name]
		self.db_driver = DBDriver(host, port)
		self.data_convert_driver = MQ_TO_DB_DRIVER()
		
	def find(self, data_format, data):
		return True
		
	def save(self, data_format, data):
		if data_format not in DB_SUPPORTED_FORMATS:
			logging.info(f'Unsupported data-format to save: {data_format}')
			raise TypeError(f'Unsupported data-format to save: {data_format}')
		data_converted = self.data_convert_driver.convert(data) #dioctionary-ed and ready to go.
		self.db_driver.save(data_format, data_converted)
			
		
