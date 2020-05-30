from .cortex_pb2 import 	User, Snapshot, Pose, ColorImage, DepthImage, Feelings
from PIL import Image
import gzip
from blessings import Terminal
import datetime as dt
from furl import furl

INT_SIZE=4 
term = Terminal()
GENDERS_RMAP = {User.Gender.FEMALE:'f',User.Gender.MALE:'m', User.Gender.OTHER:'o'}
UNCOMPRESSED = 'uncompressed'
COMPRESSORS = {'gzip': gzip, 'uncompressed':'uncompressed'}


class ProtoReaderDriver:
	
	def __init__(self, fd):
		self.fd = fd
		self.current_snapshot_length_b = b''
	
	def read_user_information(self):
		length_byte = self.fd.read(INT_SIZE)
		user_info_length = int.from_bytes(length_byte, byteorder='little')
		user_bytes_string = self.fd.read(user_info_length)
		user = User()
		user.ParseFromString(user_bytes_string)
		return user
		
	def read_next_snapshot(self):
		''' reads next snapshot, by reading a uint32_t determining length of next snapshot
		and then reading that many bytes and putting it in a snapshot object that was pre-defined
		in a proto_file'''
		snapshot_length = int.from_bytes(self.current_snapshot_length_b, byteorder="little")
		buff = self.fd.read(snapshot_length) 
		snapshot = Snapshot()
		snapshot.ParseFromString(buff)
		return snapshot
		
	def read_all(self):
		x = self.fd.read()
		return self.fd.read()
	def next_snapshot_exists(self):
		'''this function returns True if there exists another snapshot to read, while at the same
		time putting in the instance field that length in bytes (after reading it), if not
		it returns False. implemented this way cause of proto-buf/format of file '''
		self.current_snapshot_length_b = self.fd.read(INT_SIZE)
		if len(self.current_snapshot_length_b)==0: #length of next read token means EOF.
			return False
		return True
		

READER_DRIVERS = {'protobuf': ProtoReaderDriver}

def find_compressor(furl_object):
    '''returns the compressed file format is supported. returns None if not supported'''
    comp_kind = furl_object.args['compressor']
    if comp_kind in COMPRESSORS:
        return COMPRESSORS[comp_kind]
    print(term.red('invalid URL - Reader'))
    raise ValueError(f'invalid URL: Unsupported file compression file {comp_kind}')

def find_reader_driver(furl_object):
    driver = furl_object.scheme
    if driver in READER_DRIVERS:
        return READER_DRIVERS[driver]
    print(term.red('invalid URL - Reader'))
    raise ValueError(f'invalid URL: Unsupported reading file format {driver}')
    
class Reader:
	'''this class defined an abstraction to a Reader reading a file.
	it supports differnet compression formats, as well as different sample formats
	Usage:
		Reader object is initiated with a URL like: 'SCHEME://PATH/?compressor=COMP'
		SCHEME being the sample format, example: Protobuf
		PATH being the path to the sample format
		COMP being the compression format of the file, example : gzip or uncompressed (for non-compressed files)
		
	to add another sample parsing foramt (SCHEME), you have to implement read_user_information, read_next_snapshot and
	next_snapshot_exists() functions. object needs to be initiated by opened file-descriptor
	
	to add another compression format (COMP), you have to implement a decompressing object, that implements
	open and close function. open fucking allowing to read byte-by-bye '''
	
	def open_file(self):
		if self.compressor == UNCOMPRESSED:
			self.fd = open(self.path, "rb")
		else:
			self.fd = self.compressor.open(self.path, "rb")
	
	def close_file(self):
		self.fd.close()
		
	def __init__(self, url):
		ffurl = furl(url) 
		self.compressor = find_compressor(ffurl)
		print('X', term.red_on_white(str(ffurl.path)))
		self.path = str(ffurl.path)[:-1] #TODO, path in furl path has extra / at the end
		self.open_file() #can open path now, after extracting compression-type and file path
		
		self.reader_driver = find_reader_driver(ffurl)(self.fd) #initiating reader_driver with our file-descriptor
		self.user = self.reader_driver.read_user_information()
		
	def debug_read_all(self):
		'''debugging purposes'''
		return self.reader_driver.read_all()
		
	@property
	def user_id(self):
		return self.user.user_id
		
	def __iter__(self):
		while self.reader_driver.next_snapshot_exists()==True:
			yield self.reader_driver.read_next_snapshot()
		self.close_file()
