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
		snapshot_id = f"{user_id}_{datetime}" #the unique snapshot id is concatenation of user_id and datetime of snapshot, seperated by _
		if result_length == 1: #if first one here, then should initialize the datetime inside current snapshot document in the users' snapshots array
			self.users.update_one({"_id":user_id}, {"$push":{"snapshots":{"datetime":datetime}}})#push generates array automatically
			self.users.update_one({"_id":user_id,"snapshots.datetime":datetime},{"$set":{ "snapshots.$.snapshotId":snapshot_id}}) #insert snapshot ID for API purposes PROJECT: chose it to be the same as datetime for the sake of simplicity
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
		print(f"Data of {data_name} saved successfully.")
		
	def debug_save(self, data):
		self.users.insert_one(data)
		
	def debug_delete_id(self, user_id):
		self.users.delete_one({"_id":user_id})
	
	def fill_user_info_dic(self, dic, userId, username, birthday, gender):
		if userId:
			dic['user_info.userId']=1
		if username:
			dic['user_info.username']=1
		if birthday:
			dic['user_info.birthday']=1
		if gender:
			dic['user_info.gender']=1
			
	def load_users(self, userId=0, username=0, birthday=0, gender=0):
		'''Parameters indicate which info of users to return, this function is used both by
		api and gui modules. '''
		search_dic = {"_id":0}
		self.fill_user_info_dic(search_dic,userId,username,birthday,gender)
		return self.users.find({},search_dic)
		
	def load_user_info(self, user_id):
		debug= self.users.find_one({"_id":user_id}, {"user_info":1, "_id":0})
		return debug
		
	def fill_search_dic(self, dic, datetime, snapshotId, feelings, pose, color_image, depth_image):
		if datetime:
			dic["snapshots.datetime"]=1
		if snapshotId:
			dic["snapshots.snapshotId"]=1
		if feelings:
			dic["snapshots.feelings"]=1
		if pose:
			dic["snapshots.pose"]=1
		if color_image:
			dic["snapshots.color_image"]=1
		if depth_image:
			dic["snapshots.depth_image"]=1
		
	def load_user_snapshots_list(self,user_id, datetime=0,snapshotId=0,feelings=0, pose=0, color_image=0, depth_image=0):
		search_dic = {"_id":0}
		self.fill_search_dic(search_dic, datetime, snapshotId, feelings, pose, color_image, depth_image)
		return self.users.find_one({"_id":user_id}, search_dic) 
	
	def load_user_snapshot(self, user_id, snapshot_id):
		debug = self.users.find_one({"snapshots.snapshotId":snapshot_id}, {"_id":0, "snapshots":{"$elemMatch":{"snapshotId":snapshot_id}}})
		return debug
		
	def load_feelings_result(self, user_id, snapshot_id):
		feelings_result = self.users.find_one({"snapshots.snapshotId":snapshot_id}, {"_id":0, "snapshots":{"$elemMatch":{"snapshotId":snapshot_id}}, "snapshots.snapshotId":0, "snapshots.pose":0, "snapshots.color_image":0, "snapshots.depth_image":0, "user_info":0, "snapshots.datetime":0}) #there could be a prettier way
		return feelings_result
		
	def load_color_image_result(self, user_id, snapshot_id):
		result = self.users.find_one({"snapshots.snapshotId":snapshot_id}, {"_id":0, "snapshots":{"$elemMatch":{"snapshotId":snapshot_id}}, "snapshots.snapshotId":0, "snapshots.pose":0, "snapshots.feelings":0, "snapshots.depth_image":0, "user_info":0, "snapshots.datetime":0}) 
		return result
		
	def load_depth_image_result(self, user_id, snapshot_id):
		result = self.users.find_one({"snapshots.snapshotId":snapshot_id}, {"_id":0, "snapshots":{"$elemMatch":{"snapshotId":snapshot_id}}, "snapshots.snapshotId":0, "snapshots.pose":0, "snapshots.feelings":0, "snapshots.color_image":0, "user_info":0, "snapshots.datetime":0}) 
		return result
		
	def load_pose_result(self, user_id, snapshot_id):
		result = self.users.find_one({"snapshots.snapshotId":snapshot_id}, {"_id":0, "snapshots":{"$elemMatch":{"snapshotId":snapshot_id}}, "snapshots.snapshotId":0, "snapshots.depth_image":0, "snapshots.feelings":0, "snapshots.color_image":0, "user_info":0, "snapshots.datetime":0}) 
		return result


class JsonToMongo():
	'''this driver converts from the MQ format to the DB Driver format
	in our case, the MQ protocol is json and the driver is mongo
	the driver expected python dictionaries, so simple json.loads sufficies.
	for more complicated formats other than json that might have been used, this
	class could be benefitial '''
	def convert(self, data):
		return json.loads(data)

class MongoToJson(): #this class is very related to the api, consider moving it there
	'''This driver converts from DB format to python dictionary for the purpose of API.
	in our cause, this converting-driver expects cursor of MONGODB type, and processes them
	according to python-dictionary '''
	def convert_users_list(self, cursor):
		array = list(cursor) #returns list of user_info : {relevant fields}
		smaller_array = [array[i]['user_info'] for i in range(len(array))] #getting rid of the user_info field
		return smaller_array
		
	def convert_user_info(self, result):
		'''Here we don't process much, the resut of the MongoDriver's loa_user_info is already a dictionary.
		we just need to get rid of the header and retreive the nested dictionary only. '''
		if result == None:
			print("User specified not found.")
			return {}
		return result['user_info']
	def convert_user_snapshots_list(self,result):
		if result == None:
			print("snapshots non-existent")
			return {}
		return result['snapshots']
		
	def convert_user_snapshot(self, result):
		snapshot = result['snapshots'][0]
		clean_snapshot = snapshot.copy()
		clean_snapshot.pop('datetime')
		clean_snapshot.pop('snapshotId')
		
		available_results = [key for key in clean_snapshot if len(clean_snapshot[key])>0 ] #length of a result menaing its not empty, hence available in the current snapshot
																						   #POJECT: put them in list, set is not Json-serializable
		return_dic = {"datetime":snapshot['datetime'], "snapshotId":snapshot['snapshotId']}
		return_dic["results"] = available_results
		return return_dic
		
	def result_easy_convert(self, result):
		'''This is somewhat-general in the DB-TO-PYTHON-DICTIONARY for results in this 
		convert driver. the data by nature is a dictionary of values, so it just returns the
		relevant data from the returned struture (also python-dict) of the mongoDriver for it
		to be used by the api_get methods '''
		print(result)
		return result['snapshots'][0]

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
			raise TypeError(f'Unsupported data-format to save: {data_format}')
		data_converted = self.data_convert_driver.convert(data) #dioctionary-ed and ready to go.
		self.db_driver.save(data_format, data_converted)
	def load_users(self, userId=0, username=0, birthday=0, gender=0):
		data_retreived = self.db_driver.load_users(userId, username, birthday, gender)
		users_list_json = self.db_to_api_driver.convert_users_list(data_retreived)
		return users_list_json
		
	def load_user_info(self, user_id):
		data_retreived = self.db_driver.load_user_info(user_id)
		specific_user_info = self.db_to_api_driver.convert_user_info(data_retreived)
		return specific_user_info
	
	def load_user_snapshots_list(self, user_id, datetime=0,snapshotId=0,feelings=0, pose=0, color_image=0, depth_image=0):
		data_retreived = self.db_driver.load_user_snapshots_list(user_id, datetime=datetime, snapshotId=snapshotId, feelings=feelings, pose=pose, color_image=color_image, depth_image=depth_image)
		user_snapshots_list = self.db_to_api_driver.convert_user_snapshots_list(data_retreived)
		return user_snapshots_list
		
	def load_user_snapshot_results(self, user_id, snapshot_id):
		'''This function, with the help of db_driver, loads information of a specific snapshot, and returns a dictionary
		containing the available results to be used in the API'''
		data_retreived = self.db_driver.load_user_snapshot(user_id, snapshot_id)
		return_dic = self.db_to_api_driver.convert_user_snapshot(data_retreived)
		return return_dic
		
	def load_user_result(self, user_id, snapshot_id, result_name):
		if result_name == "feelings": #can't use DB_SUPPORTED_FORMATS cause of name-inconsistency.
			data_retreived = self.db_driver.load_feelings_result(user_id, snapshot_id)	
			data_converted = self.db_to_api_driver.result_easy_convert(data_retreived)
		elif result_name == "pose":
			data_retreived = self.db_driver.load_pose_result(user_id, snapshot_id)
			data_converted = self.db_to_api_driver.result_easy_convert(data_retreived)
			
		elif result_name == "color-image":
			data_retreived = self.db_driver.load_color_image_result(user_id, snapshot_id)
			data_converted = self.db_to_api_driver.result_easy_convert(data_retreived)
		
		elif result_name == "depth-image":
			data_retreived = self.db_driver.load_depth_image_result(user_id, snapshot_id)
			data_converted = self.db_to_api_driver.result_easy_convert(data_retreived)
		else:
			print(f"Format given -{result_name}- not supported by our program.")
			return {}
		return data_converted
		
	def debug_save(self, data):
		'''This funcion saves userid, user info and a snapshot for debug purposes '''
		self.db_driver.debug_save(data)
		
	def debug_delete_id(self, user_id):
		'''This function removes data from the db by a user_id, that was inserted for debug purposes'''
		self.db_driver.debug_delete_id(user_id)
	
		
