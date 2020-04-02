from cortex_pb2 import 	User, Snapshot, Pose, ColorImage, DepthImage, Feelings
from PIL import Image
import datetime as dt
TIMESTAMP_SIZE = 8
INT_SIZE = 4
CHAR_SIZE = 1
COORDINATE_SIZE = 8
BGR_SIZE = 3
FLOAT_SIZE = 4
GENDERS_RMAP = {User.Gender.FEMALE:'f',User.Gender.MALE:'m', User.Gender.OTHER:'o'}

def read_user_information(fd):
	'''receives file descriptor, and reads user information from it
	wraps it in a User object that was extracted
	from .protobuf file'''
	
	length_byte = fd.read(INT_SIZE)
	user_info_length = int.from_bytes(length_byte, byteorder='little')
	user_bytes_string = fd.read(user_info_length)
	user = User()
	user.ParseFromString(user_bytes_string)
	return user
	

class Reader:
	'''Class Reader, reads through a sample and is convenient.
	no need to open or close file after reading. default format is protobuf.
	allows different compression formats as long as it has an appropriate open method
	support command-line-interface functionality.'''
	
	def open_file(self, compress):
		if compress == gzip:
			self.fd = gzip.open(self.path, "rb")
		elif compress == None:
			self.fd = open(self.path, "rb")
		else:
			logging.error("Unsupported compressed file")
			raise TypeError('Unsupported compressed file')
			
	def close_file(self):
		self.fd.close()
		
	def __init__(self, path, compress=None, frmt="proto"):
		self.path = path
		self.open_file(compress)
		if frmt == "proto":
			self.proto_init_metadata()
		else:
			logging.error("Reading format not supported")
			raise TypeError("Reading format not supported")
			
	def proto_init_metadata(self):
		self.user = read_user_information(self.fd)
		self.user_id = self.user.user_id
		self.username = self.user.username
		self.birthday = self.user.birthday
		self.gender = GENDERS_RMAP[self.user.gender] #self.gender is a single character
		
	def __iter__(self):
		while True:
			snapshot_length_b = self.fd.read(INT_SIZE)
			if snapshot_length_b == b'':
				break
			snapshot_length = int.from_bytes(snapshot_length_b, byteorder="little")
			buff = fd.read(snapshot_length) #TODO: consider taking less bytes at once
			snapshot = Snapshot()
			snapshot.ParseFromString(buff)
			yield snapshot
